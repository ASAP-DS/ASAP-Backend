# Generated by Django 3.2.9 on 2021-11-12 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_click_recomms'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='ID',
            new_name='login_ID',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='PW',
            new_name='login_PW',
        ),
    ]