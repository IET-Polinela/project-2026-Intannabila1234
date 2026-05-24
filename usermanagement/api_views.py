from rest_framework import generics, permissions
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """API endpoint for citizen registration.

    - Anyone may register (AllowAny)
    - Password is write-only and will be hashed by `set_password`
    """

    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
