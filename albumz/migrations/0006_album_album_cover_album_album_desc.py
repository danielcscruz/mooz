# Generated by Django 5.1.3 on 2024-12-01 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albumz', '0005_alter_album_edit_permissions_alter_foto_fotografo'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='album_cover',
            field=models.ImageField(blank=True, null=True, upload_to='album_covers/'),
        ),
        migrations.AddField(
            model_name='album',
            name='album_desc',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]