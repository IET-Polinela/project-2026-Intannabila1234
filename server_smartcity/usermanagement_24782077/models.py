from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended user: is_admin untuk petugas kota, is_member untuk warga."""
    is_admin  = models.BooleanField(default=False)
    is_member = models.BooleanField(default=True)

    def __str__(self):
        return self.username
