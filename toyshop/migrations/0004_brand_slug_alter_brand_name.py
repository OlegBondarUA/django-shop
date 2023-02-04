# Generated by Django 4.1.5 on 2023-02-04 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toyshop', '0003_remove_brand_name_en_alter_brand_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
