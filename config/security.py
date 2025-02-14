from datetime import timedelta

# 🔐 HTTPS xavfsizligi
SECURE_SSL_REDIRECT = True  # HTTP orqali kelgan so‘rovlarni HTTPS ga o‘tkazish uchun
SECURE_HSTS_SECONDS = 31536000  # 1 yilga HSTS yoqadigan qilamiz
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Subdomenga ham qo‘llashimiz mumkin
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True

CORS_ALLOW_CREDENTIALS = False
CORS_ORIGIN_ALLOW_ALL = False  # XSS hujumlaridan himoya devori

# 🔐 Cookie xavfsizligi
SESSION_COOKIE_SECURE = True  # Faqat HTTPS orqali ishlaydiagn qilamiz
CSRF_COOKIE_SECURE = True  # CSRF faqat HTTPS orqali ishlaydigan qilamiz
CSRF_COOKIE_HTTPONLY = True  # CSRF tokenni faqat server o‘qiy oladi qilamiz
X_FRAME_OPTIONS = "DENY"  # Clickjacking hujumlaridan himoya devorini qoyamiz

# 🔐 JSON Web Token (JWT) sozlamalarini sozlab olamiz
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": "SECRET_KEY",
    "AUTH_HEADER_TYPES": ("Bearer",),
}
