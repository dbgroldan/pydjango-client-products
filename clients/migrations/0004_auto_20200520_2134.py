# Generated by Django 3.0.6 on 2020-05-20 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_client_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='id',
        ),
        migrations.AlterField(
            model_name='client',
            name='document',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
