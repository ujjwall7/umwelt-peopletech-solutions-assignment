# Generated by Django 4.2.16 on 2024-09-28 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0002_alter_enrollee_enrollee_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollee',
            name='experience',
            field=models.CharField(choices=[('Has relevent experience', 'Has relevent experience'), ('No relevent experience', 'No relevent experience')], max_length=150),
        ),
    ]
