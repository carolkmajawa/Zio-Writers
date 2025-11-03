from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    SignUpView,
    LoginView,
    LogoutView,
    RequestPasswordReset,
    VerifyResetCodeAndChangePassword,
    SendEmailVerificationView,
    VerifyEmailTokenView,
    CodeVerificationView,
    PasswordResetVerifyCodeView,
)




router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),

    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password-reset/request/', RequestPasswordReset.as_view(), name='password_reset_request'),
    # path('password-reset/verify/', PasswordResetVerifyCodeView.as_view(), name='password_reset_verify'),
    path('password-reset/confirm/', VerifyResetCodeAndChangePassword.as_view(), name='password_reset_confirm'),

    path('email-verification/send/', SendEmailVerificationView.as_view(), name='email_verification_send'),
    path('email-verification/verify/', VerifyEmailTokenView.as_view(), name='email_verification_verify'),

    path('code-verification/', CodeVerificationView.as_view(), name='code_verification'),
]
