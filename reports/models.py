from django.db import models
from django.conf import settings


class Report(models.Model):
    STATUS_DRAFT = 'DRAFT'
    STATUS_VERIFIED = 'VERIFIED'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_VERIFIED, 'Verified'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='api_reports'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.reporter})"
