# Generated by Django 3.2 on 2021-05-17 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0019_alter_userpost_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpost',
            name='image',
            field=models.ImageField(null=True, upload_to='user_post'),
        ),
    ]
