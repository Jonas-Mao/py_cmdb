# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2023-12-11 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServerUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
                ('username', models.CharField(max_length=32, verbose_name='系统用户')),
                ('password', models.CharField(max_length=32, verbose_name='系统密码')),
                ('info', models.TextField(verbose_name='备注')),
            ],
            options={
                'permissions': (('add_serveruser', '添加资产用户'), ('show_serveruser', '查看资产用户'), ('delete_serveruser', '删除资产用户'), ('update_serveruser', '更新资产用户')),
                'default_permissions': [],
            },
        ),
    ]
