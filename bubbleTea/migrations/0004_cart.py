# Generated by Django 5.0.4 on 2024-04-18 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bubbleTea', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]