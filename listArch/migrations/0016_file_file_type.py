# Generated by Django 2.2.13 on 2020-08-14 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listArch', '0015_auto_20200814_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_type',
            field=models.TextField(blank=True, null=True, verbose_name='Dosya Tipi'),
        ),
    ]
