# Generated by Django 4.1.5 on 2023-01-22 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('category', models.CharField(choices=[('Electronics', 'Electronics'), ('Food', 'Food'), ('Stationary', 'Stationary')], max_length=50, null=True)),
                ('quantity', models.PositiveIntegerField(null=True)),
            ],
        ),
    ]
