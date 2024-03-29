# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2023-12-11 19:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_serveruser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='硬盘名字')),
                ('size', models.CharField(max_length=32, verbose_name='硬盘大小')),
            ],
        ),
        migrations.CreateModel(
            name='NetWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='网卡名字')),
                ('ip_address', models.CharField(max_length=32, verbose_name='网卡地址')),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=32, verbose_name='主机名')),
                ('cpu_info', models.CharField(max_length=100, verbose_name='CPU信息')),
                ('cpu_count', models.IntegerField(verbose_name='CPU个数')),
                ('mem_info', models.CharField(max_length=32, verbose_name='内存信息')),
                ('os_system', models.CharField(max_length=32, verbose_name='系统平台')),
                ('os_system_num', models.IntegerField(verbose_name='系统平台位数')),
                ('uuid', models.CharField(max_length=64, verbose_name='uuid')),
                ('sn', models.CharField(max_length=100, verbose_name='sn')),
                ('scan_status', models.IntegerField(choices=[(0, '连接异常'), (1, '连接正常')], verbose_name='探测状态')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建主机时间')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新主机时间')),
            ],
        ),
        migrations.AddField(
            model_name='network',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.Server'),
        ),
        migrations.AddField(
            model_name='disk',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.Server'),
        ),
    ]
