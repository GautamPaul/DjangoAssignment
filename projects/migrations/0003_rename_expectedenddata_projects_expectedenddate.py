# Generated by Django 3.2.5 on 2021-08-18 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_release'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projects',
            old_name='expectedEndData',
            new_name='expectedEndDate',
        ),
    ]
