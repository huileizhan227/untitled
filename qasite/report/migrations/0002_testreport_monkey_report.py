# Generated by Django 2.1.5 on 2019-10-29 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testreport',
            name='monkey_report',
            field=models.FileField(default=None, null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
    ]
