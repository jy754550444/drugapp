# coding=utf-8
# Create your views here.
import json,datetime
from django.shortcuts import render, render_to_response, HttpResponse
import io
from rest_framework.response import Response
from rest_framework.views import APIView
from .check import create_validate_code
from django.http import HttpResponseRedirect
from .models import DrugStock, DrugPurchase, DrugSale,Category
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .serializers import DrugStockListSerializer,CategorySerializer

# 后台自动获取数据ajax
def admins(request):
    id = request.GET.get('drugid')
    all_data = DrugStock.objects.get(id=id)
    retValue = {'model': all_data.model,'unit':all_data.unit.id, 'manufacturer': all_data.manufacturer, 'register_code': all_data.register_code}
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
def stock_list(request):
    context = {
        "categorys": Category.objects.all()
    }
    return render_to_response('stock_list.html', context)


#采购查询列表
def purchase_list(request):
    username = request.session['username']
    data = DrugPurchase.objects.all()
    return render_to_response('storage_list.html',{'storage_data':data, 'username': username,})


#销售查询列表
def sale_list(request):
    username = request.session['username']
    data = DrugSale.objects.all()
    return render_to_response('sale_list.html',{'sale_data':data, 'username': username,})





#库存查询列表
class DrugStockListView(APIView):

    def get(self, request, format=None):

        catid = request.GET.get("catid")
        start = int(request.GET['start'])
        length = int(request.GET['length'])
        draw = int(request.GET['draw'])

        columnList = ('name', 'category', 'unit', 'model', 'manufacturer', 'register_code', 'stock_count')
        #排序
        order_column = request.GET.get("order[0][column]")

        #asc desc 升序或者降序
        order_dir = request.GET['order[0][dir]']
        if order_column:
            ordercol = columnList[int(order_column)]
            if order_dir == "desc":
                ordercol = "-" + ordercol

        queryset_list = DrugStock.objects.order_by(ordercol)

        recordsTotal = queryset_list.count()
        #搜索
        search = request.GET.get("search[value]")

        #类型（首先判断有子类）
        if catid and int(catid) > 0:

            parents = Category.objects.get(id=catid)

            children = parents.get_children().count()
            descendant = parents.get_descendant_count()

            cats = Category.objects.filter(parent=catid)

            if cats.count() > 0:
                queryset_list = queryset_list.filter(category__parent=catid)
            else:
                queryset_list = queryset_list.filter(category__id=catid)

        if search and len(search) > 0:
            queryset_list = queryset_list.filter(
                Q(name__icontains=search) |
                Q(category__name__icontains=search) |
                Q(unit__name__icontains=search) |
                Q(model__icontains=search) |
                Q(manufacturer__icontains=search) |
                Q(register_code__icontains=search) |
                Q(stock_count__icontains=search)
            )

        recordsFiltered = queryset_list.count()

        queryset_list = queryset_list[start:(start + length)]

        serializer = DrugStockListSerializer(queryset_list,many=True)

        resp = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': recordsFiltered,
            'data': serializer.data,
        }

        return Response(resp)

    # def post(self,request,format=None):
    #     if request.method =="POST":
    #         objects = Administrations.objects.all()
    #
    #         recordsTotal = objects.count()
    #         recordsFiltered = recordsTotal
    #         start = int(request.POST['start'])
    #         length = int(request.POST['length'])
    #         draw = int(request.POST['draw'])
    #         objects = objects[start:(start + length)]
    #
    #


# 销售统计
def sale_count(request):
    limit = 0
    limit1 = 0
    limit2 = 0
    limit3 = 0
    limit4 = 0
    limit5 = 0
    username = request.session['username']
    time_now = datetime.datetime.now().strftime("%Y-%m-%d", )
    time_now1 = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    time_now2 = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%Y-%m-%d", )
    time_now3 = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d", )
    time_now4 = (datetime.datetime.now() + datetime.timedelta(days=4)).strftime("%Y-%m-%d", )
    time_now5 = (datetime.datetime.now() + datetime.timedelta(days=5)).strftime("%Y-%m-%d", )
    datas = DrugSale.objects.filter(create_time__contains=time_now)
    for i in datas:
        limit += i.sale_count
    datas1 = DrugSale.objects.filter(create_time__contains=time_now1)
    for i in datas1:
        limit1 += i.sale_count
    datas2 = DrugSale.objects.filter(create_time__contains=time_now2)
    for i in datas2:
        limit2 += i.sale_count
    datas3 = DrugSale.objects.filter(create_time__contains=time_now3)
    for i in datas3:
        limit3 += i.sale_count
    datas4 = DrugSale.objects.filter(create_time__contains=time_now4)
    for i in datas4:
        limit4 += i.sale_count
    datas5 = DrugSale.objects.filter(create_time__contains=time_now5)
    for i in datas5:
        limit5 += i.sale_count
    return render_to_response('sale_count.html',
                              {'username': username, 'time_now': time_now, 'time_now1':time_now1,
                               'time_now2': time_now2, 'time_now3': time_now3, 'time_now4': time_now4,
                               'time_now5': time_now5, 'limti': limit, 'limit1': limit1, 'limit2': limit2,
                               'limit3': limit3, 'limit4': limit4, 'limit5': limit5}, )




# 采购统计
def purchase_count(request):
    limit = 0
    limit1 = 0
    limit2 = 0
    limit3 = 0
    limit4 = 0
    limit5 = 0
    username = request.session['username']
    time_now = datetime.datetime.now().strftime("%Y-%m-%d", )
    time_now1 = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    time_now2 = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%Y-%m-%d", )
    time_now3 = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d", )
    time_now4 = (datetime.datetime.now() + datetime.timedelta(days=4)).strftime("%Y-%m-%d", )
    time_now5 = (datetime.datetime.now() + datetime.timedelta(days=5)).strftime("%Y-%m-%d", )
    datas = DrugPurchase.objects.filter(create_time__contains=time_now)
    for i in datas:
        limit += i.sale_count
    datas1 = DrugPurchase.objects.filter(create_time__contains=time_now1)
    for i in datas1:
        limit1 += i.sale_count
    datas2 = DrugPurchase.objects.filter(create_time__contains=time_now2)
    for i in datas2:
        limit2 += i.sale_count
    datas3 = DrugPurchase.objects.filter(create_time__contains=time_now3)
    for i in datas3:
        limit3 += i.sale_count
    datas4 = DrugPurchase.objects.filter(create_time__contains=time_now4)
    for i in datas4:
        limit4 += i.sale_count
    datas5 = DrugPurchase.objects.filter(create_time__contains=time_now5)
    for i in datas5:
        limit5 += i.sale_count
    return render_to_response('purchase_count.html',
                              {'username': username, 'time_now': time_now, 'time_now1':time_now1,
                               'time_now2': time_now2, 'time_now3': time_now3, 'time_now4': time_now4,
                               'time_now5': time_now5, 'limti': limit, 'limit1': limit1, 'limit2': limit2,
                               'limit3': limit3, 'limit4': limit4, 'limit5': limit5}, )


# 库存统计
def stock_count(request):
    limit = 0
    limit1 = 0
    limit2 = 0
    limit3 = 0
    limit4 = 0
    limit5 = 0
    username = request.session['username']
    time_now = datetime.datetime.now().strftime("%Y-%m-%d", )
    time_now1 = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    time_now2 = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%Y-%m-%d", )
    time_now3 = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d", )
    time_now4 = (datetime.datetime.now() + datetime.timedelta(days=4)).strftime("%Y-%m-%d", )
    time_now5 = (datetime.datetime.now() + datetime.timedelta(days=5)).strftime("%Y-%m-%d", )
    datas = DrugStock.objects.filter(create_time__contains=time_now)
    for i in datas:
        limit += i.stock_count
    datas1 = DrugStock.objects.filter(create_time__contains=time_now1)
    for i in datas1:
        limit1 += i.stock_count
    datas2 = DrugStock.objects.filter(create_time__contains=time_now2)
    for i in datas2:
        limit2 += i.stock_count
    datas3 = DrugStock.objects.filter(create_time__contains=time_now3)
    for i in datas3:
        limit3 += i.stock_count
    datas4 = DrugStock.objects.filter(create_time__contains=time_now4)
    for i in datas4:
        limit4 += i.stock_count
    datas5 = DrugStock.objects.filter(create_time__contains=time_now5)
    for i in datas5:
        limit5 += i.stock_count
    return render_to_response('stock_count.html',
                              {'username': username, 'time_now': time_now, 'time_now1':time_now1,
                               'time_now2': time_now2, 'time_now3': time_now3, 'time_now4': time_now4,
                               'time_now5': time_now5, 'limti': limit, 'limit1': limit1, 'limit2': limit2,
                               'limit3': limit3, 'limit4': limit4, 'limit5': limit5}, )





