# Generated by Django 3.2.2 on 2021-05-15 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0013_alter_wordcard_last_learn_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordcard',
            name='last_learn_date',
            field=models.DateTimeField(null=True),
        ),
    ]