import random
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import User
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User, PasswordResetCode
from .serializers import ForgotPasswordSerializer, PasswordResetSerializer
from .serializers import (
    UserSerializer, LoginSerializer, ForgotPasswordSerializer,
    PasswordResetSerializer, EmailVerificationSerializer, CodeVerificationSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"error": "User account is disabled"}, status=status.HTTP_403_FORBIDDEN)

        login(request, user)
        return Response({"detail": "Logged in successfully"}, status=status.HTTP_200_OK)      

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"detail": "Logged out successfully"}, status=200)

def create_password_reset_code(user):
    # Invalidate existing valid codes before creating a new one
    PasswordResetCode.objects.filter(user=user, expires_at__gte=timezone.now()).delete()
    code = f"{random.randint(0, 999999):06d}"  # 6-digit zero-padded numeric code
    expires_at = timezone.now() + timezone.timedelta(minutes=10)
    PasswordResetCode.objects.create(user=user, code=code, expires_at=expires_at)
    return code


class RequestPasswordReset(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_active:
            return Response({"error": "User account is inactive."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.has_usable_password():
            return Response({"error": "Cannot reset password for this account."}, status=status.HTTP_400_BAD_REQUEST)

        code = create_password_reset_code(user)

        html_message = f"""
        <html>
          <body style='background:#ffe6f7; padding:18px; font-family:sans-serif; color:#b30059;'>
            <h2>Password Reset - Zio Writers</h2>
            <p>Please use the following code to reset your password:</p>
            <div style="background:#fff; text-align:center; border-radius:8px; padding:14px; margin:18px 0;
                        font-size: 32px; letter-spacing: 8px; font-weight:bold;">{code}</div>
            <p>If you did not request a password reset, please ignore this email.</p>
          </body>
        </html>
        """

        send_mail(
            subject="Your Password Reset Code",
            message="Use an email client that supports HTML to view your reset code.",
            from_email="no-reply@example.com",
            recipient_list=[email],
            fail_silently=False,
            html_message=html_message,
        )
        return Response({"message": "Reset code sent."}, status=status.HTTP_200_OK)


class VerifyResetCodeAndChangePassword(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        code = serializer.validated_data.get('code')
        new_password = serializer.validated_data.get('password')

        try:
            user = User.objects.get(email=email)
            reset_code = PasswordResetCode.objects.get(user=user, code=code)
        except (User.DoesNotExist, PasswordResetCode.DoesNotExist):
            return Response({"error": "Invalid email or code."}, status=status.HTTP_400_BAD_REQUEST)

        if reset_code.is_expired():
            return Response({"error": "Code expired."}, status=status.HTTP_400_BAD_REQUEST)

        user.password = make_password(new_password)
        user.save()
        reset_code.delete()  # Invalidate the code after successful reset

        return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)


# Additional views for email verification and code verification (optional)
class PasswordResetVerifyCodeView(generics.GenericAPIView):
    serializer_class = CodeVerificationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Implement code verification logic if needed
        return Response({"detail": "Code verified"}, status=status.HTTP_200_OK)

class SendEmailVerificationView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Implement sending email verification token logic
        return Response({"detail": "Verification email sent"}, status=status.HTTP_200_OK)

class VerifyEmailTokenView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Implement email token verification logic
        return Response({"detail": "Email verified"}, status=status.HTTP_200_OK)

class CodeVerificationView(generics.GenericAPIView):
    serializer_class = CodeVerificationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Implement generic code or OTP verification logic
        return Response({"detail": "Code verified"}, status=status.HTTP_200_OK)
