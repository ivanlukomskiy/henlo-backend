# Generated by Django 4.0.4 on 2022-05-18 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('henlo_app', '0004_translation_starred'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translation',
            name='updated',
            field=models.DateTimeField(),
        ),
    ]