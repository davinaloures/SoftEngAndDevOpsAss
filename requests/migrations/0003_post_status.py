# Generated by Django 4.0.3 on 2022-04-15 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0002_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(default='Active', max_length=100),
        ),
    ]
