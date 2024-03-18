from django.shortcuts import render
from django.views.generic import ListView,View,TemplateView
from resources.models import *
from django.http import JsonResponse
import json

# Create your views here.
class IdcListView(ListView):
    template_name = 'idc_list.html'
    model = Idc

# class IdcAddView(TemplateView):
#     template_name = 'idc_add.html'
#     def post(self,request):
#         data = request.POST
#         print(type(data),data)
#         res = {'status':0,'msg':'添加成功'}
#         try:
#             idc = Idc()
#             idc.name = data.get('name')
#             idc.name_cn = data.get('name_cn')
#             idc.address = data.get('address')
#             idc.phone = data.get('phone')
#             idc.username = data.get('username')
#             idc.username_email = data.get('username_email')
#             idc.username_phone = data.get('username_phone')
#             idc.save()
#             print(data)
#         except Exception as e:
#             print(e)
#             res = {'status': 1, 'msg': '添加失败'}
#         return JsonResponse(res)

class IdcAddView(TemplateView):
    template_name = 'idc_add.html'

    def post(self,request):
        #接收到json字符串
        data = request.body
        #转为json对象　字典
        data = json.loads(data)
        #处理不需要的数据 csrftoken
        data.pop('csrfmiddlewaretoken')
        print(data)
        res = {'status':0,'msg':'添加成功'}
        try:
            Idc.objects.create(**data)
        except Exception as e:
            print(e)
            res = {'status': 1, 'msg': '添加失败'}
        return JsonResponse(res)

class IdcUpdateView(View):
    def get(self,reqest):
        #接收需要修改的机房id
        id = reqest.GET.get('id')
        #查询出需要修改的机房信息　对象
        idc_obj = Idc.objects.get(id=id)
        return render(reqest,'idc_update.html',{'idc_obj':idc_obj})

    def post(self, request):
        data = request.POST
        res = {'status':0,'msg':'更新成功'}
        try:
            idc = Idc.objects.get(id=request.POST.get('id'))
            idc.name = data.get('name')
            idc.name_cn = data.get('name_cn')
            idc.address = data.get('address')
            idc.phone = data.get('phone')
            idc.username = data.get('username')
            idc.username_email = data.get('username_email')
            idc.username_phone = data.get('username_phone')
            idc.save()
        except Exception as e:
            print(e)
            res = {'status': 1, 'msg': '更新失败'}
        return JsonResponse(res)

class IdcDeleteView(View):
    def post(self,request):
        res = {'status':0,'msg':'删除成功'}
        idc_id = request.POST.get('id')
        print(idc_id)
        try:
            Idc.objects.get(id=idc_id).delete()
        except Idc.DoesNotExist:
            res = {'status':1,'msg':'此机房不存在，无法删除'}
        except Exception:
            res = {'status':2,'msg':'未知错误，请联系管理员处理'}
        return JsonResponse(res)

class ServerUserListView(ListView):
    template_name = 'serveruser_list.html'
    model = ServerUser

class ServerUserAddView(TemplateView):
    template_name = 'serveruser_add.html'
    def post(self,request):
        data = request.POST
        print(data)
        res = {'status': 0, 'msg': '添加成功'}
        try:
            user = ServerUser()
            user.name = data.get('name')
            user.username = data.get('username')
            user.password = data.get('password')
            user.info = data.get('info')
            user.save()
        except Exception as e:
            print(e)
            res ={'status':1,'msg':'添加失败'}
        return JsonResponse(res)

class ServerUserUpdateView(View):
    def get(self, request):
        id = request.GET.get('id')
        serveruser_obj = ServerUser.objects.get(id=id)
        return render(request,'serveruser_update.html',{'serveruser_obj':serveruser_obj})

    def post(self,request):
        data = request.POST
        res = {'status': 0, 'msg': '更新成功'}
        try:
            user = ServerUser.objects.get(id=data.get('id'))
            user.name = data.get('name')
            user.username = data.get('username')
            user.password = data.get('password')
            user.info = data.get('info')
            user.save()
        except Exception as e:
            print(e)
            res = {'status': 1, 'msg': '更新失败'}
        return JsonResponse(res)

class ServerUserDeleteView(View):
    def post(self,request):
        res = {'status': 0, 'msg': '删除成功'}
        try:
            ServerUser.objects.get(id=request.POST.get('id')).delete()
        except Exception as e:
            print(e)
            res = {'status':1,'msg':'删除失败'}
        return JsonResponse(res)

class ServerListView(ListView):
    template_name = 'server_list.html'
    model = Server

class ServerApiView(View):
    def post(self,request):
        data = request.body
        data = json.loads(data)
        res = {'status': 0, 'msg': '接收成功'}
        #添加收到的数据到主机信息表
        #处理基础信息
        try:
            try:
                server_obj = Server.objects.get(uuid=data['uuid'])
                server_obj.delete()
            except Exception as e:
                server_obj = Server()
            #删除硬盘、网卡关联信息
            server_obj.network_set.all().delete()
            server_obj.disk_set.all().delete()
            server_obj.hostname = data['hostname']
            server_obj.cpu_info = data['cpu_info']
            server_obj.cpu_count = data['cpu_count']
            server_obj.mem_info = data['mem_info']
            server_obj.os_system = data['os_system']
            server_obj.os_system_num = data['os_system_num']
            server_obj.uuid = data['uuid']
            server_obj.sn = data['sn']
            server_obj.scan_status = 1
            server_obj.save()
            #网卡信息
            for k,v in data['ip_info'].items():
                NetWork.objects.create(
                    name = k,
                    ip_address = v,
                    server = server_obj
                )
            #硬盘信息
            for k,v in data['disk_info'].items():
                Disk.objects.create(
                    name = k,
                    size = v,
                    server = server_obj
                )
        except Exception as e:
            print(e)
            res = {'status': 1, 'msg': '接收失败'}
        return JsonResponse(res)
