# Generated by Django 3.0.3 on 2020-04-09 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0003_auto_20200408_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='correct',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
