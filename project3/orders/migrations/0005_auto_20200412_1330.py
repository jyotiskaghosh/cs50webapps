# Generated by Django 3.0.5 on 2020-04-12 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20200412_1255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='menu',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='orders.Menu'),
        ),
    ]