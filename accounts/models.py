# This code defines a custom user model with a custom user manager, along with an OTP model for
# generating and validating one-time passwords.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager #managaerdan CustomManagerni chqirib oldim
from .utils import is_otp_valid # utilsdan qoshimcha maydonni chqirib oldim




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



    def __str__(self):
        return f"OTP for {self.user.email} - {self.otp_code}"
