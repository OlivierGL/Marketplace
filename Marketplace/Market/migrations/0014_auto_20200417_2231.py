# Generated by Django 3.0.4 on 2020-04-18 02:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Market', '0013_merge_20200416_0520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='glassart',
            name='product',
        ),
        migrations.RemoveField(
            model_name='jewelry',
            name='product',
        ),
        migrations.RemoveField(
            model_name='painting',
            name='product',
        ),
        migrations.RemoveField(
            model_name='sculpture',
            name='product',
        ),
        migrations.DeleteModel(
            name='Garment',
        ),
        migrations.DeleteModel(
            name='GlassArt',
        ),
        migrations.DeleteModel(
            name='Jewelry',
        ),
        migrations.DeleteModel(
            name='Painting',
        ),
        migrations.DeleteModel(
            name='Sculpture',
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
