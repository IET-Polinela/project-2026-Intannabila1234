from django.conf import settings
from django.db import models


class Report(models.Model):
    """Laporan warga untuk portal Smart City."""

    STATUS_DRAFT    = 'DRAFT'
    STATUS_REPORTED = 'REPORTED'
    STATUS_DIPROSES = 'DIPROSES'
    STATUS_SELESAI  = 'SELESAI'

    STATUS_CHOICES = [
        (STATUS_DRAFT,    'Draft'),
        (STATUS_REPORTED, 'Reported'),
        (STATUS_DIPROSES, 'Diproses'),
        (STATUS_SELESAI,  'Selesai'),
    ]

    title       = models.CharField(max_length=255)
    category    = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField()
    reporter    = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='api_reports',
    )
    status     = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} — {self.reporter} [{self.status}]"
