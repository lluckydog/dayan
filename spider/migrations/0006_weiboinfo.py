# Generated by Django 3.1 on 2021-02-15 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spider', '0005_auto_20210213_1201'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeiboInfo',
            fields=[
                ('id', models.CharField(help_text='微博id', max_length=20, primary_key=True, serialize=False, verbose_name='微博id')),
                ('user_id', models.CharField(help_text='用户id', max_length=20, verbose_name='用户id')),
                ('nickname', models.CharField(help_text='用户昵称', max_length=30, verbose_name='用户昵称')),
                ('text', models.CharField(help_text='微博正文', max_length=3000, verbose_name='微博正文')),
                ('created_at', models.DateTimeField(verbose_name='发布时间')),
                ('source', models.CharField(max_length=30, verbose_name='发布工具')),
                ('attitudes_count', models.IntegerField(default=0, verbose_name='点赞数')),
                ('comments_count', models.IntegerField(default=0, verbose_name='评论数')),
                ('reposts_count', models.IntegerField(default=0, verbose_name='转发数')),
                ('keyword', models.CharField(max_length=100, verbose_name='搜索关键词')),
            ],
            options={
                'verbose_name': '微博信息',
                'verbose_name_plural': '微博信息',
            },
        ),
    ]
