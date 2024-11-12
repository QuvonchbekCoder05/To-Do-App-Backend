from .contrib.auth.models import BaseUserManager


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
