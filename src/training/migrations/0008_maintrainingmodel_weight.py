# Generated by Django 5.1.4 on 2024-12-13 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0007_alter_subtrainingmodel_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintrainingmodel',
            name='weight',
            field=models.CharField(default=0, max_length=10),
        ),
    ]