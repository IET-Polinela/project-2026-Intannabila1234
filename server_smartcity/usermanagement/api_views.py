from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer

User = get_user_model()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Login menggunakan email + password (bukan username)."""

    email    = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hapus field 'username' bawaan SimpleJWT
        self.fields.pop(self.username_field, None)

    def validate(self, attrs):
        email    = attrs.get('email', '').strip()
        password = attrs.get('password', '')

        if not email or not password:
            raise serializers.ValidationError(
                {'detail': _('Email dan password harus diisi.')}
            )

        user = User.objects.filter(email__iexact=email).first()
        if user is None:
            raise serializers.ValidationError(
                {'detail': _('Email atau password salah.')}
            )

        auth_user = authenticate(username=user.username, password=password)
        if auth_user is None:
            raise serializers.ValidationError(
                {'detail': _('Email atau password salah.')}
            )
        if not auth_user.is_active:
            raise serializers.ValidationError(
                {'detail': _('Akun nonaktif.')}
            )

        attrs['username'] = auth_user.username
        attrs['password'] = password
        return super().validate(attrs)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
    permission_classes = (permissions.AllowAny,)


class RegisterView(generics.CreateAPIView):
    """Registrasi warga baru. Terbuka untuk umum (AllowAny)."""
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
