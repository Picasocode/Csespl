# Generated by Django 5.0.6 on 2024-05-27 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_rename_research_project_research_paper'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='research_paper',
        ),
        migrations.AddField(
            model_name='project',
            name='research_outcome',
            field=models.CharField(choices=[('IEEE Conference', 'IEEE Conference'), ('Springer Conference ', 'Springer Conference'), ('Scopus Conference', 'Scopus Conference'), ('Scopus Journals', 'Scopus Journals'), ('SCI Journals', 'SCI Journals'), ('Patent', 'Patent')], default='Patent', max_length=100),
        ),
    ]