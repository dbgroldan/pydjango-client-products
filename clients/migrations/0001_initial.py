# Generated by Django 3.0.6 on 2020-05-20 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('document', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=100)),
            ],
        ),
    ]
