# Generated by Django 5.1.4 on 2024-12-17 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0011_subtrainingmodel_help_training'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtrainingmodel',
            name='total_weight',
            field=models.FloatField(default=0.0, verbose_name='合計重量'),
        ),
    ]