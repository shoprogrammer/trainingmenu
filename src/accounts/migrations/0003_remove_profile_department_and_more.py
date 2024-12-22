# Generated by Django 5.1.4 on 2024-12-16 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='department',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='profile',
            name='affiliation',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='所属'),
        ),
        migrations.AddField(
            model_name='profile',
            name='height',
            field=models.IntegerField(blank=True, null=True, verbose_name='身長'),
        ),
        migrations.AddField(
            model_name='profile',
            name='total_score',
            field=models.IntegerField(blank=True, null=True, verbose_name='合計重量'),
        ),
        migrations.AddField(
            model_name='profile',
            name='weight',
            field=models.IntegerField(blank=True, null=True, verbose_name='体重'),
        ),
    ]