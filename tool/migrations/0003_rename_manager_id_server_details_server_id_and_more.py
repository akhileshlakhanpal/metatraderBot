# Generated by Django 5.1.4 on 2025-01-12 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0002_copier_details_password_master_details_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='server_details',
            old_name='manager_id',
            new_name='server_id',
        ),
        migrations.RenameField(
            model_name='server_details',
            old_name='server_port',
            new_name='server_password',
        ),
    ]
