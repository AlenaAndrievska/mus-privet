# Generated by Django 4.2.16 on 2024-11-05 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musprivet', '0026_alter_blog_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicesongsvideo',
            name='video_url',
        ),
        migrations.RemoveField(
            model_name='servicevideoadvertisement',
            name='video_url',
        ),
        migrations.AddField(
            model_name='servicesongsvideo',
            name='video_file',
            field=models.FileField(blank=True, null=True, upload_to='video/', verbose_name='видео файл'),
        ),
        migrations.AddField(
            model_name='servicevideoadvertisement',
            name='video_file',
            field=models.FileField(blank=True, null=True, upload_to='video/', verbose_name='видео файл'),
        ),
    ]
