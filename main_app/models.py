from django.db import models

class Report(models.Model):
    STATUS_CHOICES = [
        ('REPORTED', 'REPORTED'),
        ('VERIFIED', 'VERIFIED'),
        ('IN_PROGRESS', 'IN_PROGRESS'),
        ('RESOLVED', 'RESOLVED'),
    ]

    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    def __str__(self):
        return f"{self.title} - {self.status}"