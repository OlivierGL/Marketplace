# Generated by Django 3.0.4 on 2020-04-14 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_auto_20200414_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='is_default_shipping',
            field=models.BooleanField(default=False),
        ),
    ]