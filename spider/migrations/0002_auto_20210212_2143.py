# Generated by Django 3.1 on 2021-02-12 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spider', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='verified_reason',
            field=models.CharField(blank=True, max_length=100, verbose_name='认证'),
        ),
    ]
