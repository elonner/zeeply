# Generated by Django 4.2.1 on 2023-06-05 22:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0009_alter_skill_enddate_alter_skill_startdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=400, null=True)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('rating', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('followers', models.ManyToManyField(related_name='follower', to=settings.AUTH_USER_MODEL)),
                ('following', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='curr_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
