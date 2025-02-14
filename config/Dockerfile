# 1️⃣ Python 3.12 versiyasini ishlatamiz
FROM python:3.12

# 2️⃣ Loyihaning ichida ishlash uchun papka yaratamiz
WORKDIR /app

# 3️⃣ Barcha fayllarni Docker konteyneriga nusxalash
COPY . /app

# 4️⃣ Kerakli kutubxonalarni o‘rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Django static fayllarni yig‘amiz
RUN python manage.py collectstatic --noinput

# 6️⃣ Gunicorn orqali serverni ishga tushiramiz
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
