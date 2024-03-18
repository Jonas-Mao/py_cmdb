# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2023-12-10 23:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Idc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='机房简称')),
                ('name_cn', models.CharField(max_length=32, verbose_name='机房名称')),
                ('address', models.CharField(max_length=64, verbose_name='机房地址')),
                ('phone', models.CharField(max_length=11, verbose_name='机房座机电话')),
                ('username', models.CharField(max_length=32, verbose_name='机房负责人姓名')),
                ('username_email', models.EmailField(max_length=254, verbose_name='机房负责人邮箱')),
                ('username_phone', models.CharField(max_length=11, verbose_name='机房负责人手机号')),
            ],
            options={
                'permissions': (('add_idc', '添加IDC'), ('show_idc', '查看IDC'), ('delete_idc', '删除IDC'), ('update_idc', '更新IDC')),
                'default_permissions': [],
            },
        ),
    ]
