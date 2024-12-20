# Generated by Django 4.2.16 on 2024-10-01 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musprivet', '0011_subcategory_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceadvertisement',
            name='category',
        ),
        migrations.RemoveField(
            model_name='servicevideoadvertisement',
            name='category',
        ),
        migrations.AddField(
            model_name='tag',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_tags', to='musprivet.subcategory'),
        ),
        migrations.AlterField(
            model_name='serviceadvertisement',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_ads', to='musprivet.subcategory'),
        ),
        migrations.AlterField(
            model_name='servicevideoadvertisement',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_video_ads', to='musprivet.subcategory'),
        ),
    ]
