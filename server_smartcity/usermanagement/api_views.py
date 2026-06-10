from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer


User = get_user_model()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop(self.username_field, None)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError({'detail': _('Email dan password harus diisi.')})

        user = User.objects.filter(email__iexact=email).first()
        if user is None:
            raise serializers.ValidationError({'detail': _('Email atau password salah.')})

        authenticated_user = authenticate(username=user.username, password=password)
        if authenticated_user is None:
            raise serializers.ValidationError({'detail': _('Email atau password salah.')})
        if not authenticated_user.is_active:
            raise serializers.ValidationError({'detail': _('User nonaktif.')})

        attrs['username'] = authenticated_user.username
        attrs['password'] = password

        return super().validate(attrs)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
    permission_classes = (permissions.AllowAny,)


class RegisterView(generics.CreateAPIView):
    """API endpoint for citizen registration.

    - Anyone may register (AllowAny)
    - Password is write-only and will be hashed by `set_password`
    """

    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
