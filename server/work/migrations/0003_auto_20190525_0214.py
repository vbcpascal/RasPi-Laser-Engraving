# Generated by Django 2.2.1 on 2019-05-24 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0002_auto_20190525_0206'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='user',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='text',
            name='user',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
