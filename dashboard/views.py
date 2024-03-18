from django.shortcuts import render
from django.views.generic import View,TemplateView
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
# Create your views here.

# class IndexView(View):
#     def get(self, request):
#         return render(request,'index.html',{'body':'这是首页面'})

class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['body'] = '这是首页面'
        return context

class LoginView(TemplateView):
    template_name = 'login.html'
    # def post(self,request):
    #     data = request.POST
    #     #校验用户和密码
    #     if data.get('username') == 'admin' and data.get('password') == '123456':
    #         res = {'status':0, 'msg':'登陆成功'}
    #     else:
    #         res = {'status':1, 'msg':'用户名或密码错误'}
    #     return JsonResponse(res)

    def post(self,request):
        data = request.POST
        #校验用户和密码
        #会自动连接数据库进行校验
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user:
            #登陆成功　写会话信息 session
            res = {'status':0, 'msg':'登陆成功'}
            login(request, user)
        else:
            res = {'status':1, 'msg':'用户名或密码错误'}
        return JsonResponse(res)

class LogoutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('user_login'))