# Generated by Django 3.0.5 on 2020-04-12 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20200412_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='pizza',
            name='menu_item',
        ),
        migrations.RemoveField(
            model_name='sub',
            name='menu_item',
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='menu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='orders.Menu'),
        ),
        migrations.AlterField(
            model_name='topping',
            name='pizza',
            field=models.ManyToManyField(blank=True, related_name='toppings', to='orders.MenuItem'),
        ),
        migrations.DeleteModel(
            name='DinnerPlatter',
        ),
        migrations.DeleteModel(
            name='Pizza',
        ),
        migrations.DeleteModel(
            name='Sub',
        ),
        migrations.AddField(
            model_name='variation',
            name='menu_item',
            field=models.ManyToManyField(related_name='variations', to='orders.MenuItem'),
        ),
    ]
