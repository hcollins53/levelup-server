# Generated by Django 4.2 on 2023-04-26 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0003_event_date_event_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='date',
        ),
        migrations.AddField(
            model_name='event',
            name='date_and_time',
            field=models.CharField(default='Monday at 7pm', max_length=200),
        ),
    ]
