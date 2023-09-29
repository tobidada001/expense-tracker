# Generated by Django 4.1 on 2023-09-28 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='')),
                ('category', models.CharField(max_length=50, verbose_name='')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='')),
            ],
        ),
    ]
