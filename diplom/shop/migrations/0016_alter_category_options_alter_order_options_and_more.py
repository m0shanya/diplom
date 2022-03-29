# Generated by Django 4.0.1 on 2022-03-29 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_order_cost_order_count_order_purchase_delete_buy'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('title',), 'verbose_name': 'Category', 'verbose_name_plural': 'Category'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-created_at',), 'verbose_name': 'Order', 'verbose_name_plural': 'Order'},
        ),
        migrations.AddField(
            model_name='order',
            name='delivery',
            field=models.CharField(max_length=13, null=True),
        ),
    ]
