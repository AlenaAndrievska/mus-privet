# Generated by Django 4.2.16 on 2024-09-26 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='name')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Мужской'), ('F', 'Женский')], max_length=1)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='name')),
                ('city', models.CharField(db_index=True, max_length=100, verbose_name='city')),
                ('text', models.TextField(verbose_name='text')),
            ],
            options={
                'verbose_name': 'review',
                'verbose_name_plural': 'reviews',
                'db_table': 'review',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('is_male_name_related', models.BooleanField(default=False)),
                ('is_female_name_related', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='musprivet.category')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
                'db_table': 'tag',
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='name')),
                ('category', models.ForeignKey(max_length=100, on_delete=django.db.models.deletion.CASCADE, related_name='subcategory', to='musprivet.category')),
            ],
            options={
                'verbose_name': 'subcategory',
                'verbose_name_plural': 'subcategories',
                'db_table': 'subcategory',
            },
        ),
        migrations.CreateModel(
            name='ServiceSongs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('format_type', models.CharField(choices=[('audio', 'Audio'), ('video', 'Video')], max_length=5)),
                ('media_file', models.FileField(upload_to='media/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services_songs', to='musprivet.category')),
            ],
            options={
                'verbose_name': 'song',
                'verbose_name_plural': 'songs',
                'db_table': 'song',
            },
        ),
        migrations.CreateModel(
            name='ServiceCongrats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('audio_file', models.FileField(blank=True, null=True, upload_to='audio/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services_congrats', to='musprivet.category')),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='musprivet.name')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musprivet.tag')),
            ],
            options={
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
                'db_table': 'service',
            },
        ),
        migrations.CreateModel(
            name='ServiceAdvertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('format_type', models.CharField(choices=[('audio', 'Audio'), ('video', 'Video')], max_length=5)),
                ('media_file', models.FileField(upload_to='media/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='musprivet.category')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services_advertisement', to='musprivet.subcategory')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musprivet.tag')),
            ],
            options={
                'verbose_name': 'advertisement',
                'verbose_name_plural': 'advertisement',
                'db_table': 'advertisement',
            },
        ),
    ]
