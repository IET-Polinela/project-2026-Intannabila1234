import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title',       models.CharField(max_length=255)),
                ('category',    models.CharField(blank=True, default='', max_length=100)),
                ('description', models.TextField()),
                ('status', models.CharField(
                    choices=[
                        ('DRAFT',    'Draft'),
                        ('REPORTED', 'Reported'),
                        ('DIPROSES', 'Diproses'),
                        ('SELESAI',  'Selesai'),
                    ],
                    default='DRAFT',
                    max_length=20,
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reporter', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='api_reports',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={'ordering': ['-updated_at']},
        ),
    ]
