# Generated by Django 4.2.16 on 2024-10-02 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musprivet', '0015_serviceadclipprice_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicevideoadvertisement',
            name='video_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
