# Generated by Django 4.0.4 on 2022-04-26 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0005_alter_spam_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='global',
            name='registeruser',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='myapi.registerusers'),
        ),
    ]