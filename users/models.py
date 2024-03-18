from django.db import models
from django.contrib.auth.models import User,Group

# Creates your models here.
class Profile(models.Model):
    name_cn = models.CharField(max_length=50,verbose_name='中文名')
    wechat = models.CharField(max_length=50,verbose_name='微信')
    phone = models.CharField(max_length=11,verbose_name='电话')
    info = models.TextField(verbose_name='备注')
    profile = models.OneToOneField(User)

    class Meta:
        default_permissions = []
        permissions = (
            ('user_add','添加用户'),
            ('user_show','查看用户'),
            ('user_update','修改用户'),
            ('user_delete','删除用户')
        )

class NewGroup(Group):
    class Meta:
        default_permissions = []
        permissions = (
            ('group_add', '添加用户组'),
            ('group_show', '查看用户组'),
            ('group_update', '修改用户组'),
            ('group_delete', '删除用户组')
        )
