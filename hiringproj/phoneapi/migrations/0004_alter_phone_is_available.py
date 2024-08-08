# Generated by Django 5.1 on 2024-08-08 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phoneapi', '0003_alter_phone_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='is_available',
            field=models.BooleanField(choices=[(True, 'موجود'), (False, 'ناموجود')], default=True, verbose_name='موجودی'),
        ),
    ]
