# Generated by Django 3.2 on 2021-05-13 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0011_alter_donation_info_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation_info',
            name='hospital',
            field=models.CharField(default=' ', max_length=50),
        ),
    ]