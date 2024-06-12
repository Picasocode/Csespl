# Generated by Django 5.0.6 on 2024-06-12 03:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_alter_projectmember_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='documents/')),
                ('ppt', models.FileField(upload_to='ppts/')),
                ('status', models.CharField(choices=[('not_verified', 'Not Verified'), ('verified', 'Verified')], default='not_verified', max_length=20)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='project.project')),
            ],
        ),
    ]
