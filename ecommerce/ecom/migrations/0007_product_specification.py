# Generated by Django 5.0 on 2024-01-26 07:39

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0006_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='specification',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]
