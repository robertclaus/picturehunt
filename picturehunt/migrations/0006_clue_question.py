# Generated by Django 2.1.7 on 2019-08-29 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picturehunt', '0005_auto_20190818_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='clue',
            name='question',
            field=models.TextField(blank=True, null=True),
        ),
    ]