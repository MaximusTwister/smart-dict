# Generated by Django 3.2.2 on 2021-05-15 11:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0016_alter_wordcard_last_learn_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordcard',
            name='last_learn_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
