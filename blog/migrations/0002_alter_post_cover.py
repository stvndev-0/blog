# Generated by Django 5.0.6 on 2024-06-19 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cover',
            field=models.ImageField(null=True, upload_to='image/'),
        ),
    ]