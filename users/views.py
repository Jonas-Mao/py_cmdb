from django.shortcuts import render
from django.views.generic import View,ListView,TemplateView
from django.contrib.auth.models import User,Group,Permission
from users.models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required,permission_required

# Create your views here.
# class UserListView(View):
#     def get(self,request):
#         data = User.objects.all()
#         return render(request,'user_list.html',{'data':data})
class UserListView(LoginRequiredMixin,ListView):
    template_name = 'user_list.html'
    model = User
    paginate_by = 8
    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['page_range'] = self.page_range(context['page_obj'],context['paginator'])
        print(context)
        return context
    def page_range(self,page_obj,paginator):
        current_page = page_obj.number
        start = current_page - 2
        end = current_page + 3
        #限制显示范围　如果小于第一页　就从第一页开始取
        if start < 1:
            start = 1
        #如果大于总页数　就取到最大页数
        if end > paginator.num_pages:
            end = paginator.num_pages + 1
        #如果取出页数后发现没有5页
        current_page_num = end - start
        #把end往后取　前面少几页　往后加几页
        #如果end是最大页数　取完了　后面也没有
        if (end == paginator.num_pages + 1):
            start = start - (5 - current_page_num)
        else:
        #如果取出页面不够5页　后面还有页面可取　就补齐
            if current_page_num < 5:
                end = end + (5 -current_page_num)
        return range(start,end)

#添加用户数据测试分布
class TestDataView(View):
    def get(self, request):
        for i in range(1, 100):
            user = User()
            profile = Profile()
            user.username = 'user{}'.format(i)
            user.password = make_password('123456')
            user.email = '{}.qq@com'.format(i)
            user.save()
            profile.profile_id = user.id
            profile.name_cn = '用户{}'.format(i)
            profile.wechat = 'wechat_user{}'.format(i)
            profile.phone = '133333333{}'.format(i)
            profile.info = '测试用户{}'.format(i)
            profile.save()

class UserAddView(TemplateView):
    template_name = 'user_add.html'
    #要求先登录
    @method_decorator(login_required())
    @method_decorator(permission_required('users.user_add'))
    def get(self,request):
        return render(request, 'user_add.html')
    def post(self,request):
        data = request.POST
        res = {'status':0,'msg':'添加成功'}
        try:
            user = User()
            profile = Profile()
            user.username = data.get('username')
            user.password = make_password(data.get('password'))
            user.email = data.get('email')
            user.save()
            profile.profile_id = user.id
            profile.name_cn = data.get('name_cn')
            profile.wechat = data.get('wechat')
            profile.phone = data.get('phone')
            profile.info = ''
            profile.save()
        except Exception as e:
            print(e)
            res = {'status':1,'msg':'添加失败'}
        return JsonResponse(res)

class UserUpdateView(View):
    def get(self,request):
        print('----------',User.objects.get(id=request.GET.get('id')))
        return render(request,'user_update.html',{'user_obj':User.objects.get(id=request.GET.get('id'))})
    def post(self,request):
        data = request.POST
        res = {'status':0,'msg':'修改成功'}
        try:
            user = User.objects.get(id=data.get('uid'))
            profile = Profile.objects.get(profile_id=data.get('uid'))
            user.username = data.get('username')
            user.password = make_password(data.get('password'))
            user.email = data.get('email')
            user.save()
            profile.profile_id = user.id
            profile.name_cn = data.get('name_cn')
            profile.wechat = data.get('wechat')
            profile.phone = data.get('phone')
            profile.info = ''
            profile.save()
        except Exception as e:
            print(e)
            res = {'status':1,'msg':'修改失败'}
        return JsonResponse(res)

class UserDeleteView(View):
    def get(self,request):
        data = request.GET
        res = {'status':0,'msg':'删除成功'}
        try:
            User.objects.get(id=data.get('id')).delete()
        except Exception as e:
            print(e)
            res = {'status': 1, 'msg': '删除失败'}
        return JsonResponse(res)

class UserStatusView(View):
    def get(self,request):
        data = request.GET
        res = {'status':0,'msg':'用户状态更新成功'}
        #查询用户当前状态
        user = User.objects.get(id=data.get('id'))
        status = user.is_active
        #确定用户更新的新状态
        if status == 0:
            newstatus = 1
        else:
            newstatus = 0
        try:
            user = User.objects.get(id=data.get('id'))
            user.is_active = newstatus
            user.save()
        except Exception as e:
            print(e)
            res = {'status': 1, 'msg': '用户状态更新失败'}
        return JsonResponse(res)

class GroupListView(ListView):
    template_name = 'group_list.html'
    model = Group

class GroupAddView(ListView):
    template_name = 'group_add.html'
    model = User
    def post(self,request):
        data = request.POST
        print(data)
        res = {'status':0, 'msg':'添加成功'}
        try:
            group = Group()
            group.name = data.get('name')
            group.save()
            #此用户组添加对应的用户id
            for i in data.getlist('group_user'):
                print(i)
                #组对象反向到user对象　添加多对多的关系
                group.user_set.add(User.objects.get(id=i))
        except Exception as e:
            print(e)
            res = {'status': 1, 'msg': '添加失败'}
        return JsonResponse(res)

class GroupUpdateView(ListView):
    template_name = 'group_update.html'
    model = User
    def get_context_data(self, **kwargs):
        context = super(GroupUpdateView,self).get_context_data(**kwargs)
        context['group_obj'] = Group.objects.get(id=self.request.GET.get('id'))
        return context
    def post(self,request):
        data = request.POST
        print(data)
        res = {'status':0, 'msg':'更新成功'}
        try:
            group = Group.objects.get(id=data.get('gid'))
            group.name = data.get('name')
            group.save()
            #清空组和用户的关系
            group.user_set.clear()
            #此用户组添加对应的用户id
            for i in data.getlist('group_user'):
                print(i)
                #组对象反向到user对象　添加多对多的关系
                group.user_set.add(User.objects.get(id=i))
        except Exception as e:
            print(e)
            res = {'status': 1, 'msg': '更新失败'}
        return JsonResponse(res)

class PermListView(ListView):
    template_name = 'perm_list.html'
    model = Permission
    paginate_by = 8
    #权限名称默认英文　重写模板类的get_queryset方法
    def get_queryset(self):
        queryset = super(PermListView,self).get_queryset()
        queryset = queryset.exclude(name__regex='[a-zA-Z]')
        return queryset

class UserSetPermView(ListView):
    template_name = 'user_set_perm.html'
    model = Permission
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(UserSetPermView,self).get_context_data(**kwargs)
        context['user_obj'] = User.objects.get(id=self.request.GET.get('id'))
        return context

    #权限名称默认英文　重写模板类的get_queryset方法
    def get_queryset(self):
        queryset = super(UserSetPermView,self).get_queryset()
        queryset = queryset.exclude(name__regex='[a-zA-Z]')
        return queryset
    def post(self,request):
        data = request.POST
        print(data)
        res = {'status':0,'msg':'设置成功'}
        try:
            #获取到用户对象
            user = User.objects.get(id=data.get('uid'))
            #添加权限关系
            user.user_permissions = data.getlist('perm_list[]')
            user.save()
        except Exception as e:
            print(e)
            res = {'status': 1, 'msg': '设置失败'}
        return JsonResponse(res)