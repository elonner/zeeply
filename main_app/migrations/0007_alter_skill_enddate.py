# Generated by Django 4.2.1 on 2023-06-05 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_alter_post_rating_alter_skill_enddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='endDate',
            field=models.DateField(blank=True, null=True, verbose_name='end of skill experience'),
        ),
    ]