from django.utils import timezone


def is_valid(self):


        return timezone.now() <= self.expires_at # Hozirgi vaqt tugash vaqtidan oldin yoki teng bo'lsa True qaytaradigan qilib qoyamiz
