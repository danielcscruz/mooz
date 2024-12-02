# Generated by Django 5.1.3 on 2024-12-01 21:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albumz', '0004_album_edit_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='edit_permissions',
            field=models.ManyToManyField(blank=True, related_name='editable_albums', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='foto',
            name='fotografo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]