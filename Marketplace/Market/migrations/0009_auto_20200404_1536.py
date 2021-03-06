# Generated by Django 3.0.3 on 2020-04-07 20:38

import Market.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0008_product_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='cartproduct',
            old_name='cart_id',
            new_name='cart',
        ),
        migrations.RenameField(
            model_name='cartproduct',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='chat',
            old_name='user1_id',
            new_name='user1',
        ),
        migrations.RenameField(
            model_name='chat',
            old_name='user2_id',
            new_name='user2',
        ),
        migrations.RenameField(
            model_name='garment',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='glassart',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='jewelry',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='chat_id',
            new_name='chat',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='buyer_id',
            new_name='buyer',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='seller_id',
            new_name='seller',
        ),
        migrations.RenameField(
            model_name='orderproduct',
            old_name='order_id',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='orderproduct',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='painting',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='sculpture',
            old_name='product_id',
            new_name='product',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('PAINTING', 'Painting'), ('SCULPTURE', 'Sculpture'), ('GARMENT', 'Garment'), ('JEWELRY', 'Jewelry'), ('GLASS_ART', 'Glass Art')], default='PAINTING', max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.FileField(upload_to=Market.models.get_image_path),
        ),
    ]
