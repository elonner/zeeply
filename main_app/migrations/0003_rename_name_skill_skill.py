# Generated by Django 4.2.1 on 2023-06-05 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_post_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skill',
            old_name='name',
            new_name='skill',
        ),
    ]
