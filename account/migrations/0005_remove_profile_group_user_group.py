# Generated by Django 4.1.4 on 2023-01-12 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('account', '0004_profile_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='group',
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
        ),
    ]
