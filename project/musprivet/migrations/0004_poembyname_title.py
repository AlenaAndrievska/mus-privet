# Generated by Django 4.2.16 on 2024-09-27 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musprivet', '0003_remove_servicecongratsbyname_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='poembyname',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
