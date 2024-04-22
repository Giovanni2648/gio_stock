# Generated by Django 5.0.2 on 2024-02-29 18:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_alter_category_options_alter_entry_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exit',
            name='fk_product',
        ),
        migrations.RemoveField(
            model_name='exit',
            name='fk_transaction',
        ),
        migrations.RemoveField(
            model_name='pivot_products_supplier',
            name='fk_product',
        ),
        migrations.RemoveField(
            model_name='pivot_products_supplier',
            name='fk_supplier',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='category',
        ),
        migrations.RenameModel(
            old_name='transaction',
            new_name='Transactions',
        ),
        migrations.CreateModel(
            name='Exits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('total', models.IntegerField()),
                ('product', models.ManyToManyField(to='stock.products')),
                ('transaction', models.ManyToManyField(to='stock.transactions')),
            ],
            options={
                'verbose_name': 'Exit',
                'verbose_name_plural': 'Exits',
            },
        ),
        migrations.RenameModel(
            old_name='Category',
            new_name='Categories',
        ),
        migrations.CreateModel(
            name='Suppliers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='suppliers')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('review', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.categories')),
                ('products', models.ManyToManyField(to='stock.products')),
            ],
            options={
                'verbose_name': 'Supplier',
                'verbose_name_plural': 'Suppliers',
            },
        ),
        migrations.CreateModel(
            name='Entries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('total', models.IntegerField()),
                ('fk_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.products')),
                ('transaction', models.ManyToManyField(to='stock.transactions')),
                ('supplier', models.ManyToManyField(to='stock.suppliers')),
            ],
            options={
                'verbose_name': 'Entry',
                'verbose_name_plural': 'Entries',
            },
        ),
        migrations.DeleteModel(
            name='entry',
        ),
        migrations.DeleteModel(
            name='exit',
        ),
        migrations.DeleteModel(
            name='Pivot_Products_Supplier',
        ),
        migrations.DeleteModel(
            name='Supplier',
        ),
    ]
