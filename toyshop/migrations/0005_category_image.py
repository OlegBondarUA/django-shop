# Generated by Django 4.1.5 on 2023-02-04 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toyshop', '0004_brand_slug_alter_brand_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category_image'),
        ),
    ]
