# Generated by Django 4.2 on 2023-04-26 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0002_game_number_of_players_game_skill_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.CharField(default='Come Join us', max_length=200),
        ),
    ]
