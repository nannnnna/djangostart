# Generated by Django 4.2.5 on 2023-09-25 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strsite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
