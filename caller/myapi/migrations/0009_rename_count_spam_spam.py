# Generated by Django 4.0.4 on 2022-04-30 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0008_global_spam'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spam',
            old_name='count',
            new_name='spam',
        ),
    ]