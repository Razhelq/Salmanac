# Generated by Django 2.2.1 on 2019-09-07 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shpacoo_portal', '0007_auto_20190831_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='pictures/', verbose_name='Artist picture'),
        ),
    ]
