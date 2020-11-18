# Generated by Django 3.1.3 on 2020-11-18 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsefile', '0002_auto_20201118_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='data',
            field=models.FileField(blank=True, null=True, upload_to='data_original/', verbose_name='파일'),
        ),
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(max_length=200, verbose_name='파일명'),
        ),
    ]