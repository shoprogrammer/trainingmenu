# Generated by Django 5.1.4 on 2024-12-11 23:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0002_rename_training_subtrainingmodel_training_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subtrainingmodel',
            old_name='training_id',
            new_name='training',
        ),
    ]