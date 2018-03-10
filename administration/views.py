# coding=utf-8
# Create your views here.
import json
from django.shortcuts import render, render_to_response, HttpResponse
import io
from .check import create_validate_code
from django.http import HttpResponseRedirect
from .models import DrugStock, DrugPurchase, DrugSale
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt


# 后台自动获取数据ajax
def admins(request):
    data = request.GET.get('typename')
    all_data = DrugStock.objects.get(drugs_id=data)
    retValue = {'model': all_data.model, 'manufacturer': all_data.manufacturer, 'register_code': all_data.register_code}
    return HttpResponse(json.dumps(retValue), content_type="application/json")


# 获取验证码
def CheckCode(request):
    mstream = io.BytesIO()
    validate_code = create_validate_code()
    img = validate_code[0]
    img.save(mstream, "GIF")

    # 将验证码保存到session
    request.session["CheckCode"] = validate_code[1]

    return HttpResponse(mstream.getvalue())


# 登陆
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pad = request.POST.get('pad')
        request.session['username'] = request.POST.get('username', '')
        user = authenticate(username=username, password=pad)
        if user is not None:
            check_code = request.POST.get('checkcode')
            # 从session中获取验证码
            session_code = request.session["CheckCode"]
            if check_code.strip().lower() != session_code.lower():
                return HttpResponse('验证码不匹配')
            else:
                return HttpResponseRedirect('/index/')
        else:
            return HttpResponse('用户名或密码不正确')

    return render_to_response('login.html')


# from django.contrib.auth import logout as auth_logout
# #用户退出
# def logout(request):
#     auth_logout(request)
#     return render_to_response('login.html')


# 首页
def index(request):
    username = request.session['username']
    data = DrugStock.objects.all().order_by('-update_time')[:10]
    sale_data = DrugSale.objects.all().order_by('-update_time')[:10]
    purchase_data = DrugPurchase.objects.all().order_by('-update_time')[:10]
    return render_to_response('index.html', {'datas': data, 'username': username, 'sale_data': sale_data,
                                             'storage_data': purchase_data})


#库存查询列表
def admin_list(request):
    username = request.session['username']
    data = DrugStock.objects.all()
    return render_to_response('admin_list.html',{'datas':data,'username': username,})


#采购查询列表
def storage_list(request):
    username = request.session['username']
    data = DrugPurchase.objects.all()
    return render_to_response('storage_list.html',{'storage_data':data, 'username': username,})


#销售查询列表
def sale_list(request):
    username = request.session['username']
    data = DrugSale.objects.all()
    return render_to_response('sale_list.html',{'sale_data':data, 'username': username,})
