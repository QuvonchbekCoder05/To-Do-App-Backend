# This code defines a custom user model with a custom user manager, along with an OTP model for
# generating and validating one-time passwords.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):# Foydalanuvchilar modelini boshqarish.
    def create_user(self, email, username, password=None, **other_fields):
        if not email:
            raise ValueError("Provide email") # # Emailning mavjudligini tekshirib olamiz 
        email = self.normalize_email(email) ## Email manzilini normallashtirish uchun normileze metodina foydalanamiz 
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password) # Parolni Django'ning hashlash funksiyasi yordamida o'rnatib olamiz 
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **other_fields): #Admin huquqlariga ega superfoydalanuvchini yaratish
        other_fields.setdefault('is_staff', True) # Superuser uchun is_staff ni True ga o'rnatib qoyamiz 
        other_fields.setdefault('is_superuser', True)  # Superuser uchun is_superuserni ham truega ornatib qoyamiz admin bolishi uchun
        other_fields.setdefault('is_active', True)# Superuser  faolligini ta'minlashni amslhs odhiramiz 
        return self.create_user(email, username, password, **other_fields)

class User(AbstractBaseUser, PermissionsMixin): #  AbstractBaseUser va PermissionsMixin'dan meros oladigan moslashtirilgan foydalanuvchi modelini yaratib olamiz 
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True, blank=True, default='default_user')
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False) # # Foydalanuvchi hisobining faol ekanligini ko'rsatadigan qismi agar faol bo;lsa
    is_staff = models.BooleanField(default=False)  # Foydalanuvchining admin saytiga kirish huquqini ko'rsatadi
    is_admin = models.BooleanField(default=False) # Qo'shimcha admin funksiyalari uchun maxsus maydon yaratib olamiz 

    USERNAME_FIELD = 'email' # Avtorizatsiya uchun yagona identifikator sifatida emailni belgilab qoyamiz 
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() <= self.expires_at # Hozirgi vaqt tugash vaqtidan oldin yoki teng bo'lsa True qaytaradigan qilib qoyamiz

    def __str__(self):
        return f"OTP for {self.user.email} - {self.otp_code}"
