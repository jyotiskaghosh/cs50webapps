# Generated by Django 2.2.12 on 2020-04-17 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_variation_order_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='description',
            field=models.CharField(default='enter description', max_length=100),
        ),
    ]