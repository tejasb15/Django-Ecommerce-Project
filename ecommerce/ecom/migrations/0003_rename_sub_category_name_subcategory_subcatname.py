# Generated by Django 5.0 on 2024-01-24 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0002_subcategory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcategory',
            old_name='sub_category_name',
            new_name='subcatname',
        ),
    ]
