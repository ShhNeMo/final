# Generated by Django 4.2.4 on 2023-08-17 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_alter_item_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
