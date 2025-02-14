import decimal
from decimal import Decimal

from deep_translator import GoogleTranslator
from django.db.models import DecimalField, F, Value

from dashboard.models import SiteVisit
from products.models.conversion import Conversion


def get_conversion_rates():
    """Valyuta kursini  olamiz admindan"""
    conversion = Conversion.objects.first()
    return {
        "usd_to_uzs": Decimal(conversion.som_value) if conversion else Decimal(1),
        "uzs_to_usd": (
            Decimal(1) / Decimal(conversion.som_value)
            if conversion and conversion.som_value
            else Decimal(1)
        ),
    }


def translate_text(text, dest_language):
    """Deep Translator orqali matnni tarjima qilish logikasi"""
    if not text:
        return None
    try:
        translated_text = GoogleTranslator(
            source="auto", target=dest_language
        ).translate(text)
        print(f" Tarjima: {text} → {translated_text}")  # Log
        return translated_text
    except Exception as e:
        print(f" Tarjima xatosi roy berdi : {e} | Matn: {text} | Til: {dest_language}")
        return None


def translate_and_store(instance, fields):
    changed = False

    for field_uz, field_ru in fields:
        value_uz = (
            getattr(instance, field_uz, "") or ""
        )  # Agar None bo‘lsa, "" bosh stringa ozgartiadigan qilamiz
        value_ru = getattr(instance, field_ru, "") or ""

        if not value_uz.strip() and value_ru.strip():
            translated_text = translate_text(value_ru, "uz")
            if translated_text:
                setattr(instance, field_uz, translated_text)
                changed = True
                print(f" Tarjima qilindi: {field_uz} = {translated_text}")

        elif not value_ru.strip() and value_uz.strip():
            translated_text = translate_text(value_uz, "ru")
            if translated_text:
                setattr(instance, field_ru, translated_text)
                changed = True
                print(f" Tarjima qilindi: {field_ru} = {translated_text}")

    if changed:
        instance.save()


def filter_by_language(queryset, lang, fields):
    lang_suffix = "_uz" if lang == "uz" else "_ru"
    annotations = {}

    for field, field_options in fields.items():
        field_uz, field_ru = field_options
        annotations[field] = F(field_uz) if lang == "uz" else F(field_ru)

    return queryset.annotate(**annotations)


def apply_currency_conversion(queryset, currency, rates):
    """Narxni valyutaga mos ravishda konvertatsiya qilish uchun logika"""
    if currency == "uzs":
        return queryset.annotate(
            converted_price=F("price")
            * Value(
                rates["usd_to_uzs"],
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
    elif currency == "usd":
        return queryset.annotate(
            converted_price=F("price")
            * Value(
                rates["uzs_to_usd"],
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
    return queryset


def convert_price(price, currency, rates):
    """Oddiy qiymat uchun valyuta konvertatsiyasi alohida qilamiz bu oddiy Decimalda ishlaydi Queryda emas"""
    if currency == "uzs":
        return price * decimal.Decimal(str(rates["usd_to_uzs"]))
    elif currency == "usd":
        return price * decimal.Decimal(str(rates["uzs_to_usd"]))
    return price  # Agar boshqa valyuta bo‘lsa, o‘zgarishsiz qaytariladigan qilamiz


def count_unique_visitors(request):
    """Foydalanuvchining IP-manzilini olish va tashrifni saqlash qismi logikasi"""
    ip = get_client_ip(request)

    # IP bazada yo‘q bo‘lsa, yangi tashrif qo‘shamiz faqat bitta apinmi bir marta oladigan qilingan
    if not SiteVisit.objects.filter(ip_address=ip).exists():
        SiteVisit.objects.create(ip_address=ip)


def get_client_ip(request):
    """So‘rov yuborgan foydalanuvchining IP-manzilini olish logikasi"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")  # To‘g‘ridan-to‘g‘ri IP-manzilni olamiz
    return ip
