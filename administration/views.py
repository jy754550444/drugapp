# coding=utf-8
# Create your views here.
import json, datetime
from django.shortcuts import render, render_to_response, HttpResponse
import io
from rest_framework.response import Response
from rest_framework.views import APIView
from .check import create_validate_code
from django.http import HttpResponseRedirect
from .models import DrugStock, DrugPurchase, DrugSale, Category
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .serializers import DrugStockListSerializer, DrugPurchaseListSerializer, DrugSaleListSerializer


# 后台自动获取数据ajax
def admins(request):
    id = request.GET.get('drugid')
    all_data = DrugStock.objects.get(id=id)
    retValue = {'model': all_data.model, 'unit': all_data.unit.id, 'manufacturer': all_data.manufacturer,
                'register_code': all_data.register_code}
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
def userlogin(request):
    if request.method == 'POST':
        check_code = request.POST.get('checkcode')
        # 从session中获取验证码
        session_code = request.session["CheckCode"]
        if check_code.strip().lower() != session_code.lower():
            return HttpResponse('验证码不匹配')
        else:
            username = request.POST.get('username')
            request.session['username'] =request.POST.get('username')
            pad = request.POST.get('pad')

            user = authenticate(username=username, password=pad)
            if user is not None:
                if user.is_active:
                    login(request, user)
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
    limit_day = 0
    limit_month = 0
    limit_day_purchase = 0
    limit_month_purchase = 0
    now = datetime.datetime.now().strftime("%Y-%m-%d", )
    now_month = datetime.datetime.now()
    datas = DrugSale.objects.filter(create_time__contains=now)
    for i in datas:
        limit_day += i.sale_count
    datas_moth = DrugSale.objects.filter(create_time__month=now_month.month)
    for a in datas_moth:
        limit_month += a.sale_count
    datas_purchase = DrugPurchase.objects.filter(create_time__contains=now)
    for q in datas_purchase:
        limit_day_purchase += q.purchase_count
    datas_moth_purchase = DrugPurchase.objects.filter(create_time__month=now_month.month)
    for w in datas_moth_purchase:
        limit_month_purchase += w.purchase_count
    data = DrugStock.objects.all().order_by('-update_time')[:10]
    sale_data = DrugSale.objects.all().order_by('-update_time')[:10]
    purchase_data = DrugPurchase.objects.all().order_by('-update_time')[:10]
    return render(request, 'index.html', {'datas': data, 'sale_data': sale_data, 'limit_month': limit_month,
                                          'storage_data': purchase_data, 'limit_day': limit_day,
                                          'limit_day_purchase': limit_day_purchase,
                                          'limit_month_purchase': limit_month_purchase})


# 库存查询列表
def stock_list(request):
    context = {
        "categorys": Category.objects.all()
    }
    return render(request, 'stock_list.html', context)


# 采购查询列表
def purchase_list(request):
    context = {
        "categorys": Category.objects.all()
    }
    return render(request, 'storage_list.html', context)


# 销售查询列表
def sale_list(request):
    context = {
        "categorys": Category.objects.all()
    }
    return render(request, 'sale_list.html', context)


# 库存查询列表
class DrugStockListView(APIView):
    def get(self, request, format=None):
        catid = request.GET.get("catid")
        start = int(request.GET.get('start', '0'))
        length = int(request.GET.get('length', '0'))
        draw = int(request.GET.get('draw', '0'))

        columnList = ('name', 'category', 'unit', 'model', 'manufacturer', 'register_code', 'group', 'stock_count')
        # 排序
        order_column = request.GET.get("order[0][column]")

        # asc desc 升序或者降序
        order_dir = request.GET.get('order[0][dir]')
        if order_column:
            ordercol = columnList[int(order_column)]
            if order_dir == "desc":
                ordercol = "-" + ordercol
            queryset_list = DrugStock.objects.order_by(ordercol)
        else:
            queryset_list = DrugStock.objects.all()

        recordsTotal = queryset_list.count()
        # 搜索
        search = request.GET.get("search[value]")

        # 类型（首先判断有子类）
        if catid and int(catid) > 0:

            parents = Category.objects.get(id=catid)

            children = parents.get_children().count()
            descendant = parents.get_descendant_count()

            if children > 0 and children == descendant:
                queryset_list = queryset_list.filter(category__parent=catid)
            elif children > 0 and children != descendant:
                queryset_list = queryset_list.filter(category__parent__parent=catid)
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

        if start >= 0 and length > 0:
            queryset_list = queryset_list[start:(start + length)]

        serializer = DrugStockListSerializer(queryset_list, many=True)

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


# 销售日统计
def sale_count_day(request):
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
    que_list = [time_now, time_now1, time_now2, time_now3, time_now4, time_now5]
    for i in que_list:
        datas = DrugSale.objects.filter(create_time__contains=i)
        for a in datas:
            if a.create_time.strftime("%Y-%m-%d", ) == time_now:
                limit += a.sale_count
            if a.create_time.strftime("%Y-%m-%d", ) == time_now1:
                limit1 += a.sale_count
            if a.create_time.strftime("%Y-%m-%d", ) == time_now2:
                limit2 += a.sale_count
            if a.create_time.strftime("%Y-%m-%d", ) == time_now3:
                limit3 += a.sale_count
            if a.create_time.strftime("%Y-%m-%d", ) == time_now4:
                limit4 += a.sale_count
            if a.create_time.strftime("%Y-%m-%d", ) == time_now5:
                limit5 += a.sale_count
    return render_to_response('sale_count.html',
                              {'username': username, 'time_now': time_now, 'time_now1': time_now1,
                               'time_now2': time_now2, 'time_now3': time_now3, 'time_now4': time_now4,
                               'time_now5': time_now5, 'limti': limit, 'limit1': limit1, 'limit2': limit2,
                               'limit3': limit3, 'limit4': limit4, 'limit5': limit5}, )


# 销售月统计
def sale_count_month(request):
    limit = 0
    limit1 = 0
    limit2 = 0
    limit3 = 0
    limit4 = 0
    limit5 = 0
    limit6 = 0
    limit7 = 0
    limit8 = 0
    limit9 = 0
    limit10 = 0
    limit11 = 0
    username = request.session['username']
    que_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    for i in que_list:
        datas = DrugSale.objects.filter(create_time__month=i)
        for a in datas:
            if a.create_time.strftime("%m", ) == '01':
                limit += a.sale_count
            if a.create_time.strftime("%m") == '02':
                limit1 += a.sale_count
            if a.create_time.strftime("%m", ) == '03':
                limit2 += a.sale_count
            if a.create_time.strftime("%m", ) == '04':
                limit3 += a.sale_count
            if a.create_time.strftime("%m", ) == '05':
                limit4 += a.sale_count
            if a.create_time.strftime("%m", ) == '06':
                limit5 += a.sale_count
            if a.create_time.strftime("%m", ) == '07':
                limit6 += a.sale_count
            if a.create_time.strftime("%m") == '08':
                limit7 += a.sale_count
            if a.create_time.strftime("%m", ) == '09':
                limit8 += a.sale_count
            if a.create_time.strftime("%m", ) == '10':
                limit9 += a.sale_count
            if a.create_time.strftime("%m", ) == '11':
                limit10 += a.sale_count
            if a.create_time.strftime("%m", ) == '12':
                limit11 += a.sale_count
    return render_to_response('sale_count_month.html',
                              {'username': username, 'limti': limit, 'limit1': limit1, 'limit2': limit2,
                               'limit3': limit3, 'limit4': limit4, 'limit5': limit5, 'limti6': limit6, 'limit7': limit7,
                               'limit8': limit8,
                               'limit9': limit9, 'limit10': limit10, 'limit11': limit11}, )


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
    que_list = [time_now, time_now1, time_now2, time_now3, time_now4, time_now5]
    for i in que_list:
        datas = DrugPurchase.objects.filter(create_time__contains=i)
        for a in datas:
            if a.create_time.strftime("%Y-%m-%d", ) == time_now:
                limit += a.purchase_count
            if a.create_time.strftime("%Y-%m-%d", ) == time_now1:
                limit1 += a.purchase_count
            if a.create_time.strftime("%Y-%m-%d", ) == time_now2:
                limit2 += a.purchase_count
            if a.create_time.strftime("%Y-%m-%d", ) == time_now3:
                limit3 += a.purchase_count
            if a.create_time.strftime("%Y-%m-%d", ) == time_now4:
                limit4 += a.purchase_count
            if a.create_time.strftime("%Y-%m-%d", ) == time_now5:
                limit5 += a.purchase_count
    return render_to_response('purchase_count.html',
                              {'username': username, 'time_now': time_now, 'time_now1': time_now1,
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
    que_list = [time_now, time_now1, time_now2, time_now3, time_now4, time_now5]
    for i in que_list:
        datas = DrugStock.objects.filter(create_time__contains=i)
        for a in datas:
            if a.create_time.strftime("%Y-%m-%d", ) == time_now:
                limit += a.stock_count
            if a.create_time.strftime("%Y-%m-%d", ) == time_now1:
                limit1 += a.stock_count
            if a.create_time.strftime("%Y-%m-%d", ) == time_now2:
                limit2 += a.stock_count
            if a.create_time.strftime("%Y-%m-%d", ) == time_now3:
                limit3 += a.stock_count
            if a.create_time.strftime("%Y-%m-%d", ) == time_now4:
                limit4 += a.stock_count
            if a.create_time.strftime("%Y-%m-%d", ) == time_now5:
                limit5 += a.stock_count
    return render_to_response('stock_count.html',
                              {'username': username, 'time_now': time_now, 'time_now1': time_now1,
                               'time_now2': time_now2, 'time_now3': time_now3, 'time_now4': time_now4,
                               'time_now5': time_now5, 'limti': limit, 'limit1': limit1, 'limit2': limit2,
                               'limit3': limit3, 'limit4': limit4, 'limit5': limit5}, )


# 采购查询列表
class DrugPurchaseListView(APIView):
    def get(self, request, format=None):

        catid = request.GET.get("catid")
        start = int(request.GET.get('start', '0'))
        length = int(request.GET.get('length', '0'))
        draw = int(request.GET.get('draw', '0'))

        columnList = (
            'drugs_name', 'category', 'unit', 'model', 'manufacturer', 'register_code', 'update_time', 'group',
            'purchase_count')
        # 排序
        order_column = request.GET.get("order[0][column]")

        # asc desc 升序或者降序
        order_dir = request.GET.get('order[0][dir]')
        if order_column:
            ordercol = columnList[int(order_column)]
            if order_dir == "desc":
                ordercol = "-" + ordercol
            queryset_list = DrugPurchase.objects.order_by(ordercol)
        else:
            queryset_list = DrugPurchase.objects.all()

        recordsTotal = queryset_list.count()
        # 搜索
        search = request.GET.get("search[value]")

        # 类型（首先判断有子类）
        if catid and int(catid) > 0:

            parents = Category.objects.get(id=catid)

            children = parents.get_children().count()
            descendant = parents.get_descendant_count()

            if children > 0 and children == descendant:
                queryset_list = queryset_list.filter(drugs_name__category__parent=catid)
            elif children > 0 and children != descendant:
                queryset_list = queryset_list.filter(drugs_name__category__parent__parent=catid)
            else:
                queryset_list = queryset_list.filter(drugs_name__category__id=catid)

        if search and len(search) > 0:
            queryset_list = queryset_list.filter(
                Q(drugs_name__name__icontains=search) |
                Q(drugs_name__category__name__icontains=search) |
                Q(unit__name__icontains=search) |
                Q(model__icontains=search) |
                Q(manufacturer__icontains=search) |
                Q(register_code__icontains=search) |
                Q(purchase_count__icontains=search)
            )

        recordsFiltered = queryset_list.count()

        if start >= 0 and length > 0:
            queryset_list = queryset_list[start:(start + length)]

        serializer = DrugPurchaseListSerializer(queryset_list, many=True)

        resp = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': recordsFiltered,
            'data': serializer.data,
        }

        return Response(resp)


# 销售查询列表
class DrugSaleListView(APIView):
    def get(self, request, format=None):

        catid = request.GET.get("catid")
        start = int(request.GET.get('start', '0'))
        length = int(request.GET.get('length', '0'))
        draw = int(request.GET.get('draw', '0'))

        columnList = (
            'drugs_name', 'category', 'unit', 'model', 'manufacturer', 'register_code', 'update_time', 'group',
            'sale_count', 'customer_name', 'customer_tel')
        # 排序
        order_column = request.GET.get("order[0][column]")

        # asc desc 升序或者降序
        order_dir = request.GET.get('order[0][dir]')
        if order_column:
            ordercol = columnList[int(order_column)]
            if order_dir == "desc":
                ordercol = "-" + ordercol
            queryset_list = DrugSale.objects.order_by(ordercol)
        else:
            queryset_list = DrugSale.objects.all()

        recordsTotal = queryset_list.count()
        # 搜索
        search = request.GET.get("search[value]")

        # 类型（首先判断有子类）
        if catid and int(catid) > 0:

            parents = Category.objects.get(id=catid)

            children = parents.get_children().count()
            descendant = parents.get_descendant_count()

            if children > 0 and children == descendant:
                queryset_list = queryset_list.filter(drugs_name__category__parent=catid)
            elif children > 0 and children != descendant:
                queryset_list = queryset_list.filter(drugs_name__category__parent__parent=catid)
            else:
                queryset_list = queryset_list.filter(drugs_name__category__id=catid)

        if search and len(search) > 0:
            queryset_list = queryset_list.filter(
                Q(drugs_name__name__icontains=search) |
                Q(drugs_name__category__name__icontains=search) |
                Q(unit__name__icontains=search) |
                Q(model__icontains=search) |
                Q(manufacturer__icontains=search) |
                Q(register_code__icontains=search) |
                Q(sale_count__icontains=search) |
                Q(customer_name__icontains=search) |
                Q(customer_tel__icontains=search)
            )

        recordsFiltered = queryset_list.count()

        if start >= 0 and length > 0:
            queryset_list = queryset_list[start:(start + length)]

        serializer = DrugSaleListSerializer(queryset_list, many=True)

        resp = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': recordsFiltered,
            'data': serializer.data,
        }

        return Response(resp)
