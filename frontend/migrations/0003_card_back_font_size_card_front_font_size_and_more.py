# Generated by Django 4.2.14 on 2024-08-24 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_card_review_interval_box'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='back_font_size',
            field=models.CharField(choices=[('text-base', '216'), ('text-lg', '192'), ('text-xl', '128'), ('text-2xl', '0')], default='text-2xl', max_length=16),
        ),
        migrations.AddField(
            model_name='card',
            name='front_font_size',
            field=models.CharField(choices=[('text-base', '216'), ('text-lg', '192'), ('text-xl', '128'), ('text-2xl', '0')], default='text-2xl', max_length=16),
        ),
        migrations.AlterField(
            model_name='card',
            name='back',
            field=models.TextField(max_length=310),
        ),
        migrations.AlterField(
            model_name='card',
            name='front',
            field=models.TextField(max_length=310),
        ),
    ]
