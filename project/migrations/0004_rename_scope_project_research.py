# Generated by Django 5.0.6 on 2024-05-27 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_project_abstract'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='scope',
            new_name='research',
        ),
    ]