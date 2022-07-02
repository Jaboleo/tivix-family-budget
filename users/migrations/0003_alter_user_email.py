# Generated by Django 4.0.5 on 2022-07-02 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_name_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'A user with that username already exists'}, max_length=254, unique=True),
        ),
    ]
