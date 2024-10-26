from django.urls import path
from .views import SignUpView, VerifyOTPView, SignInView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('signin/', SignInView.as_view(), name='signin'),
]
