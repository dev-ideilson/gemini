# Generated by Django 5.2.4 on 2025-07-06 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=255, unique=True)),
                ('value', models.TextField(blank=True, default='', null=True)),
            ],
            options={
                'verbose_name': 'Setting',
                'verbose_name_plural': 'Settings',
            },
        ),
    ]
