# coding=utf-8
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import Http404, JsonResponse,HttpResponse, HttpResponseRedirect
from rest_framework.utils import json
from .models import PurchaseReturn, SaleReturn
from .pagination import LimitPagination,PagePagination
#from django.http import HttpResponseRedirect
# Create your views here.
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions,authentication
from rest_framework.generics import  ListAPIView,RetrieveAPIView
from administration.models import DrugStock,DrugSale,DrugPurchase, Unit, Category
from .serializers import (
    DrugSaleSerializer,
    UnitSerializer,
    DrugStockSerializer,
    CategorySerializer,
    DrugPurchaseSerializer,
    DrugStockListSerializer,
    PurSearchSerializer,
    SaleSearchSerializer,
    PurchaseReturnSerializer,
    SaleReturnSerializer,
)
from mptt.utils import get_cached_trees


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryTreeListAPIView(APIView):
    treeItems = []
    def get(self,request,*args,**kwargs):
        roots = get_cached_trees(Category.objects.all())
        self.treeItems.clear()
        for node in roots:
            self._listNode(node)
        #print(self.treeItems)
        return Response(self.treeItems)

    def _listNode(self, node,parentDict=None):

        if not parentDict:
            parentDict = {'id':node.id,'text':node.name}
            self.treeItems.append(parentDict)

        listItem =[]
        for child in node.get_children():
            parentItem = {'id':child.id,'text':child.name}
            listItem.append(parentItem)
            parentDict['children'] = listItem
            self._listNode(child,parentItem)


@csrf_exempt
def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        request.session['username'] =request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return JsonResponse({"success":"true","url":reverse("drugadmin-index")})

        else:
            return JsonResponse({"success":"false","error":"用户名或密码不正确"})

    return render(request, 'drugadmin/druglogin.html')


@login_required(login_url="/drugadmin/")
def index(request):
    return  render(request, "drugadmin/drugindex.html")


@login_required(login_url="/drugadmin/")
def changepwd(request):
    username = request.user.username
    oldpassword = request.POST.get('oldpwd', '')
    user = authenticate(username=username, password=oldpassword)
    if user is not None and user.is_active:
        password = request.POST.get('newpwd', '')
        password2 = request.POST.get('newpwd2', '')
        if password == password2:
            user.set_password(password)
            user.save()
        else:
            return JsonResponse({"success":"false"})
    else:
         return JsonResponse({"success":"false"})
    return JsonResponse({"success":"true"})


#用户退出
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse("drugadmin-login"))

#采购入库单
@login_required(login_url="/drugadmin/")
def purchase(request):
    return  render(request, "drugadmin/drugpurchase.html")

#库存维护
@login_required(login_url="/drugadmin/")
def stock(request):
    return  render(request, "drugadmin/drugstock.html")

#采购查询
@login_required(login_url="/drugadmin/")
def pursearch(request):
    return  render(request, "drugadmin/purchase_list.html")

#采购退货
@login_required(login_url="/drugadmin/")
def purreturn(request):
    return  render(request, "drugadmin/purchase_return.html")

#销售查询
@login_required(login_url="/drugadmin/")
def salesearch(request):
    return  render(request, "drugadmin/sale_list.html")

#销售退货
@login_required(login_url="/drugadmin/")
def salereturn(request):
    return  render(request, "drugadmin/sale_return.html")

#库存查询
@login_required(login_url="/drugadmin/")
def stocksearch(request):
    return  render(request, "drugadmin/stock_list.html")


#树测试
#@login_required(login_url="/drugadmin/")
def lefttree(request):
    return  render(request, "drugadmin/treelist.html")


class UnitListAPIView(ListAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

class CompanyStockListAPIView(ListAPIView):
    queryset = DrugStock.objects.all()
    serializer_class = DrugStockSerializer

    def get_queryset(self):
        g_counts = self.request.user.groups.count()
        if g_counts > 0:
            group = self.request.user.groups.first()
            return DrugStock.objects.filter(group=group)
        return DrugStock.objects.all()

#sale 列表
class PurchaseListAPIView(APIView):
    def get(self, request):
        queryset_list = DrugPurchase.objects.all().order_by('-update_time','-id')

        g_counts = request.user.groups.count()
        if g_counts > 0:
            group = request.user.groups.first()
            queryset_list = queryset_list.filter(group=group)

        purchase_at = request.GET.get('purchase_at',None)

        if purchase_at:
            pur_date = datetime.strptime(purchase_at, "%Y-%m-%d").date()
            queryset_list = queryset_list.filter(update_time=pur_date)

        total = queryset_list.count();
       # print(total)
        pagination = PagePagination()
        queryset_list = pagination.paginate_queryset(queryset=queryset_list,request=request,view=self)
        serializer = DrugPurchaseSerializer(queryset_list, many=True)
        resp = {
            'total':total,
            'rows':serializer.data
        }
        return Response(resp)

class PurSearchAPIView(APIView):
    def get(self, request):
        queryset_list = DrugPurchase.objects.all().order_by('-update_time')

        g_counts = request.user.groups.count()
        if g_counts > 0:
            group = request.user.groups.first()
            queryset_list = queryset_list.filter(group=group)

        begin_at = request.GET.get('begin_at',None)
        end_at = request.GET.get('end_at',None)

        if begin_at and end_at:
            begin_at = datetime.strptime(begin_at, "%Y-%m-%d").date()
            end_at = datetime.strptime(end_at, "%Y-%m-%d").date()
            queryset_list = queryset_list.filter(update_time__range=(begin_at,end_at))

        cat_id = request.GET.get('cat_id',None)
        reg_code = request.GET.get('reg_code',None)
        factory = request.GET.get('factory',None)
        drugname = request.GET.get('drugname',None)
        if cat_id:
            parents = Category.objects.get(id=cat_id)

            children = parents.get_children().count()
            descendant = parents.get_descendant_count()

            if children > 0 and children == descendant:
                queryset_list = queryset_list.filter(drugs_name__category__parent=cat_id)
            elif children > 0 and children != descendant:
                queryset_list = queryset_list.filter(drugs_name__category__parent__parent=cat_id)
            else:
                queryset_list = queryset_list.filter(drugs_name__category__id=cat_id)

        if drugname:
            queryset_list = queryset_list.filter(drugs_name__name__icontains = drugname)

        if reg_code:
            queryset_list = queryset_list.filter(register_code=reg_code)

        if factory:
            queryset_list = queryset_list.filter(manufacturer__icontains=factory)
        total = queryset_list.count();
       # print(total)
        pagination = PagePagination()
        queryset_list = pagination.paginate_queryset(queryset=queryset_list,request=request,view=self)
        serializer = PurSearchSerializer(queryset_list, many=True)
        resp = {
            'total':total,
            'rows':serializer.data
        }
        return Response(resp)


#purchase 创建
class PurchaseCreateAPIView(APIView):
    def post(self, request):

        inserts = request.data.get('inserted',None)
        jsondata = json.loads(inserts)

        group = None

        user = self.request.user
        g_counts = user.groups.count()
        if g_counts > 0:
            group = user.groups.first()

        for item in jsondata:
            serializer = DrugPurchaseSerializer(data=item)
            if serializer.is_valid():
                if group:
                    serializer.save(input_owner=user,group=group)
                serializer.save(input_owner=user)

                count = serializer.validated_data['purchase_count']
                stock = serializer.validated_data['drugs_name']
                stock.stock_count += count
                stock.save()
            else:
                resp = {
                    'success':'false',
                    'errors':serializer.errors,
                }
                return Response(resp)

        resp = {
            'success':'true',

        }
        return Response(resp)

#sale 创建
class SaleCreateAPIView(APIView):
    def post(self, request):

        inserts = request.data.get('inserted',None)
        jsondata = json.loads(inserts)

        group = None

        user = self.request.user
        g_counts = user.groups.count()
        if g_counts > 0:
            group = user.groups.first()

        for item in jsondata:
            serializer = DrugSaleSerializer(data=item)
            if serializer.is_valid():
                if group:
                    serializer.save(input_owner=user,group=group)
                serializer.save(input_owner=user)

                count = serializer.validated_data['sale_count']
                stock = serializer.validated_data['drugs_name']
                stock.stock_count -= count
                stock.save()
            else:
                resp = {
                    'success':'false',
                    'errors':serializer.errors,
                }
                return Response(resp)

        resp = {
            'success':'true',

        }
        return Response(resp)

#sale 列表
class SaleListAPIView(APIView):
    def get(self, request):
        queryset_list = DrugSale.objects.all()

        g_counts = request.user.groups.count()
        if g_counts > 0:
            group = request.user.groups.first()
            queryset_list = queryset_list.filter(group=group)

        sale_at = request.GET.get('sale_at',None)
        if sale_at:
            s_date = datetime.strptime(sale_at, "%Y-%m-%d").date()
            queryset_list = queryset_list.filter(update_time=s_date)

        total = queryset_list.count();
       # print(total)
        pagination = PagePagination()
        queryset_list = pagination.paginate_queryset(queryset=queryset_list,request=request,view=self)
        serializer = DrugSaleSerializer(queryset_list, many=True)
        resp = {
            'total':total,
            'rows':serializer.data
        }
        return Response(resp)

class SaleSearchAPIView(APIView):
    def get(self, request):
        queryset_list = DrugSale.objects.all().order_by('-update_time')

        g_counts = request.user.groups.count()
        if g_counts > 0:
            group = request.user.groups.first()
            queryset_list = queryset_list.filter(group=group)

        begin_at = request.GET.get('sdate_at',None)
        end_at = request.GET.get('edate_at',None)

        if begin_at and end_at:
            begin_at = datetime.strptime(begin_at, "%Y-%m-%d").date()
            end_at = datetime.strptime(end_at, "%Y-%m-%d").date()
            queryset_list = queryset_list.filter(update_time__range=(begin_at,end_at))

        cat_id = request.GET.get('categoryid',None)
        reg_code = request.GET.get('regcode',None)
        factory = request.GET.get('from_at',None)
        drugname = request.GET.get('drug_name',None)
        if cat_id:
            parents = Category.objects.get(id=cat_id)

            children = parents.get_children().count()
            descendant = parents.get_descendant_count()

            if children > 0 and children == descendant:
                queryset_list = queryset_list.filter(drugs_name__category__parent=cat_id)
            elif children > 0 and children != descendant:
                queryset_list = queryset_list.filter(drugs_name__category__parent__parent=cat_id)
            else:
                queryset_list = queryset_list.filter(drugs_name__category__id=cat_id)

        if drugname:
            queryset_list = queryset_list.filter(drugs_name__name__icontains=drugname)

        if reg_code:
            queryset_list = queryset_list.filter(register_code=reg_code)


        if factory:
            queryset_list = queryset_list.filter(manufacturer__icontains=factory)

        user_name = request.GET.get('user_name',None)
        user_tel = request.GET.get('user_tel',None)

        if user_name:
            queryset_list = queryset_list.filter(customer_name__icontains=user_name)

        if user_tel:
            queryset_list = queryset_list.filter(customer_tel__icontains=user_tel)

        total = queryset_list.count();
       # print(total)
        pagination = PagePagination()
        queryset_list = pagination.paginate_queryset(queryset=queryset_list,request=request,view=self)
        serializer = SaleSearchSerializer(queryset_list, many=True)
        resp = {
            'total':total,
            'rows':serializer.data
        }
        return Response(resp)


#sale 详细
class SaleDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return DrugSale.objects.get(pk=pk)
        except DrugSale.DoesNotExist:
            raise Http404

    def get(self, request,*args, **kwargs):
        pk = request.GET.get('id',0)
        sale = self.get_object(pk)
        serializer = DrugSaleSerializer(sale)
        return Response(serializer.data)

#sale 更新
class SaleUpdateAPIView(APIView):

    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return DrugSale.objects.get(pk=pk)
        except DrugSale.DoesNotExist:
            raise Http404

    def post(self,request,*args, **kwargs):
        id = request.POST.get('id',0)
        print(request.user.username),
        print('post......')
        sale = self.get_object(id)
        serializer = DrugSaleSerializer(sale,data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            resp = {
                'isError':'true',
                'errors':serializer.errors,
            }

            return Response(resp)
#sale 删除
class SaleDeleteAPIView(APIView):

     def get_object(self, pk):
        try:
            return DrugSale.objects.get(pk=pk)
        except DrugSale.DoesNotExist:
            raise Http404

     def post(self, request,*args, **kwargs):
        print("delete.....")
        id = request.POST.get('id',0)
        sale = self.get_object(id)
        sale.delete()
        resp = {
                'success':'true'
            }
        return Response(resp)

#库存
class StockDetailAPIView(RetrieveAPIView):
    queryset = DrugStock.objects.all()
    serializer_class = DrugStockSerializer


class StockListAPIView(APIView):
     def get(self, request):
        queryset_list = DrugStock.objects.all().order_by('-create_time')
        g_counts = request.user.groups.count()
        if g_counts > 0:
            group = request.user.groups.first()
            queryset_list = queryset_list.filter(group=group)

        catid = request.GET.get('catid',None)
        if catid:
            parents = Category.objects.get(id=catid)
            children = parents.get_children().count()  #直接子类数量
            descendant = parents.get_descendant_count() #所有子类
            if children > 0 and children == descendant:
                queryset_list = queryset_list.filter(category__parent=catid)
            elif children > 0 and children != descendant:
                queryset_list = queryset_list.filter(category__parent__parent=catid)
            else:
                queryset_list = queryset_list.filter(category__id=catid)

        total = queryset_list.count();
        pagination = PagePagination()
        queryset_list = pagination.paginate_queryset(queryset=queryset_list,request=request,view=self)
        serializer = DrugStockListSerializer(queryset_list, many=True)
        resp = {
            'total':total,
            'rows':serializer.data
        }
        return Response(resp)

class StockSearchAPIView(APIView):
    def get(self, request):
        queryset_list = DrugStock.objects.all().order_by('-create_time')

        g_counts = request.user.groups.count()
        if g_counts > 0:
            group = request.user.groups.first()
            queryset_list = queryset_list.filter(group=group)

        cat_id = request.GET.get('categ_id',None)
        reg_code = request.GET.get('registercode',None)
        factory = request.GET.get('manufaturer',None)
        drugname = request.GET.get('drgname',None)
        if cat_id:
            parents = Category.objects.get(id=cat_id)

            children = parents.get_children().count()
            descendant = parents.get_descendant_count()

            if children > 0 and children == descendant:
                queryset_list = queryset_list.filter(category__parent=cat_id)
            elif children > 0 and children != descendant:
                queryset_list = queryset_list.filter(category__parent__parent=cat_id)
            else:
                queryset_list = queryset_list.filter(category=cat_id)

        if drugname:
            queryset_list = queryset_list.filter(name__icontains = drugname)

        if reg_code:
            queryset_list = queryset_list.filter(register_code=reg_code)

        if factory:
            queryset_list = queryset_list.filter(manufacturer__icontains=factory)
        total = queryset_list.count();
       # print(total)
        pagination = PagePagination()
        queryset_list = pagination.paginate_queryset(queryset=queryset_list,request=request,view=self)
        serializer = DrugStockListSerializer(queryset_list, many=True)
        resp = {
            'total':total,
            'rows':serializer.data
        }
        return Response(resp)


class StockCreateAPIView(APIView):
    def get_object(self, pk):
        try:
            return DrugStock.objects.get(pk=pk)
        except DrugSale.DoesNotExist:
            raise Http404

    def post(self, request):
        inserts = request.data.get('inserted',None)
        updatedData = request.data.get('updated',None)
        if inserts:
            self.jsondata = json.loads(inserts)
            resp = self.insertData(self.jsondata)
            return  Response(resp)

        if updatedData:
            self.updateJson = json.loads(updatedData)
            resp = self.updateData(self.updateJson)
            return Response(resp)

    def insertData(self,data):
        group = None

        user = self.request.user
        g_counts = user.groups.count()
        if g_counts > 0:
            group = user.groups.first()

        resp={}
        for item in data:
            serializer = DrugStockListSerializer(data=item)
            if serializer.is_valid():
                if group:
                    serializer.save(input_owner=user,group=group)
                serializer.save(input_owner=user)
            else:
                resp = {
                    'success':'false',
                    'errors':serializer.errors,
                }
                return resp

            resp = {
                'success':'true',

            }
        return resp

    def updateData(self,data):
        resp ={}
        for item in data:
            stock = self.get_object(item['id'])
            serializer = DrugStockListSerializer(stock,data=item)
            if serializer.is_valid():
                serializer.save()
            else:
                resp = {
                    'success':'false',
                    'errors':serializer.errors,
                }
                return resp

            resp = {
                'success':'true',
            }
        return resp

#sale 删除
class StockDeleteAPIView(APIView):

     def get_object(self, pk):
        try:
            return DrugStock.objects.get(pk=pk)
        except DrugSale.DoesNotExist:
            raise Http404

     def post(self, request,*args, **kwargs):

        deleted = request.data.get('deleted',None)
        jsondata = json.loads(deleted)

        for item in jsondata:
            stock = self.get_object(item['id'])
            stock.delete()
            print(stock)
            resp = {
                'success':'true',

            }
        return Response(resp)

#采购退货列表
class PurReturnListAPIView(APIView):
    def get(self, request):
        queryset_list = PurchaseReturn.objects.all().order_by('return_at')

        g_counts = request.user.groups.count()
        if g_counts > 0:
            group = request.user.groups.first()
            queryset_list = queryset_list.filter(group=group)

        pur_return_at = request.GET.get('pur_return_at',None)

        if pur_return_at:
            return_date = datetime.strptime(pur_return_at, "%Y-%m-%d").date()
            queryset_list = queryset_list.filter(return_at=return_date)

        total = queryset_list.count();
       # print(total)
        pagination = PagePagination()
        queryset_list = pagination.paginate_queryset(queryset=queryset_list,request=request,view=self)
        serializer = PurchaseReturnSerializer(queryset_list, many=True)
        resp = {
            'total':total,
            'rows':serializer.data
        }
        return Response(resp)

#采购退货保存
class PurReturnCreateAPIView(APIView):
    def post(self, request):
        inserts = request.data.get('inserted',None)
        jsondata = json.loads(inserts)
        group = None
        user = self.request.user
        g_counts = user.groups.count()
        if g_counts > 0:
            group = user.groups.first()
        for item in jsondata:
            serializer = PurchaseReturnSerializer(data=item)
            if serializer.is_valid():
                if group:
                    serializer.save(input_owner=user,group=group)
                serializer.save(input_owner=user)

                count = serializer.validated_data['return_count']
                stock = serializer.validated_data['name']
                stock.stock_count -= count
                stock.save()
            else:
                resp = {
                    'success':'false',
                    'errors':serializer.errors,
                }
                return Response(resp)

        resp = {
            'success':'true',

        }
        return Response(resp)

#销售退货列表
class SaleReturnListAPIView(APIView):
    def get(self, request):
        queryset_list = SaleReturn.objects.all().order_by('return_at')

        g_counts = request.user.groups.count()
        if g_counts > 0:
            group = request.user.groups.first()
            queryset_list = queryset_list.filter(group=group)

        sale_return_at = request.GET.get('sale_return_at',None)

        if sale_return_at:
            return_date = datetime.strptime(sale_return_at, "%Y-%m-%d").date()
            queryset_list = queryset_list.filter(return_at=return_date)

        total = queryset_list.count();
       # print(total)
        pagination = PagePagination()
        queryset_list = pagination.paginate_queryset(queryset=queryset_list,request=request,view=self)
        serializer = SaleReturnSerializer(queryset_list, many=True)
        resp = {
            'total':total,
            'rows':serializer.data
        }
        return Response(resp)


#销售退货保存
class SaleReturnCreateAPIView(APIView):
    def post(self, request):
        inserts = request.data.get('inserted',None)
        jsondata = json.loads(inserts)
        group = None
        user = self.request.user
        g_counts = user.groups.count()
        if g_counts > 0:
            group = user.groups.first()
        for item in jsondata:
            serializer = SaleReturnSerializer(data=item)
            if serializer.is_valid():
                if group:
                    serializer.save(input_owner=user,group=group)
                serializer.save(input_owner=user)

                count = serializer.validated_data['return_count']
                stock = serializer.validated_data['name']
                stock.stock_count += count
                stock.save()
            else:
                resp = {
                    'success':'false',
                    'errors':serializer.errors,
                }
                return Response(resp)

        resp = {
            'success':'true',

        }
        return Response(resp)
