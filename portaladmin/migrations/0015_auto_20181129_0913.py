# Generated by Django 2.1.1 on 2018-11-29 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portaladmin', '0014_auto_20181129_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='mdstatement',
            name='operation',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
        migrations.AddField(
            model_name='mdstatementhistory',
            name='operation',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
    ]