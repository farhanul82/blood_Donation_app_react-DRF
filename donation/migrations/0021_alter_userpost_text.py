# Generated by Django 3.2 on 2021-05-17 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0020_alter_userpost_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpost',
            name='text',
            field=models.CharField(max_length=500),
        ),
    ]