# coding=utf-8
from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import DrugStock,Category,Unit,Region,DrugSale,DrugPurchase

from mptt.admin import MPTTModelAdmin
# Register your models here.

#药品库存

class DrugStockAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'stock_count','category','unit', 'model', 'manufacturer','register_code' ]
    fields = ('name', 'bar_code', 'or_code', 'category', 'unit', 'model', 'manufacturer','register_code','stock_count',)
    search_fields = ('name','category__name','model','manufacturer','register_code')
    list_filter = ('name','category')

    def save_model(self, request, obj, form, change):
        obj.input_owner = request.user
        userobj = request.user
        if userobj.groups.count() > 0:
            groups = userobj.groups.all()
            group = Group.objects.get(pk=groups[0].id)
            obj.group = group
        obj.save()

    def get_queryset(self, request):
        qs = super(DrugStockAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            groups = request.user.groups.all()
            group = Group.objects.get(pk=groups[0].id)
            return qs.filter(group=group)

admin.site.register(DrugStock, DrugStockAdmin)

#药品类别
class CategoryAdmin(MPTTModelAdmin):
    list_display = ['name','parent']
    search_fields = ['name']
    list_filter = ('name',)

    def get_queryset(self, request):
        qs = super(CategoryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)

admin.site.register(Category, CategoryAdmin)


#计量单位
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ('name',)

    def get_queryset(self, request):
        qs = super(UnitAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)
admin.site.register(Unit,UnitAdmin)


#地区
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ('name',)

    def get_queryset(self, request):
        qs = super(RegionAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)
admin.site.register(Region,RegionAdmin)

#药品销售
class DrugSaleAdmin(admin.ModelAdmin):
    list_display = ['drugs_name','unit','model','manufacturer','register_code','customer_name','customer_tel','sale_count', 'update_time', ]
    fields = ('drugs_name', 'unit', 'model', 'manufacturer', 'register_code', 'customer_name', 'customer_tel',
              'customer_address', 'sale_count','update_time')
    search_fields = ['drugs_name','customer_name','customer_tel','model','manufacturer','register_code']
    list_filter = ('drugs_name',)

    def get_queryset(self, request):
        qs = super(DrugSaleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            groups = request.user.groups.all()
            group = Group.objects.get(pk=groups[0].id)
            return qs.filter(company_id=group)

    def save_model(self, request, obj, form, change):

        ds = DrugStock.objects.get(name=obj.drugs_name)
        if int(ds.stock_count)>int(obj.sale_count):
            ds.stock_count = int(ds.stock_count)-int(obj.sale_count)
            ds.save()
            re = super(DrugSaleAdmin,self).save_model(request, obj, form, change)
            return re

        obj.input_owner = request.user
        userobj = request.user
        if userobj.groups.count() > 0:
            groups = userobj.groups.all()
            group = Group.objects.get(pk=groups[0].id)
            obj.group = group
        obj.save()
admin.site.register(DrugSale, DrugSaleAdmin)


class DrugPurchaseAdmin(admin.ModelAdmin):
    list_display = ('drugs_name','unit','model','manufacturer','register_code','purchase_count','update_time')
    fields  = ('drugs_name','unit','model','manufacturer','register_code','purchase_count','update_time')
    search_fields = ['storage_id']
    list_filter = ('drugs_name',)

    def get_queryset(self, request):
        qs = super(DrugPurchaseAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            groups = request.user.groups.all()
            group = Group.objects.get(pk=groups[0].id)
            return qs.filter(company_id=group)

    def save_model(self, request, obj, form, change):
        obj.input_owner = request.user
        userobj = request.user
        if userobj.groups.count() > 0:
            groups = userobj.groups.all()
            group = Group.objects.get(pk=groups[0].id)
            obj.company_id = group
        obj.save()

        re = super(DrugPurchaseAdmin,self).save_model(request, obj, form, change)
        ad = DrugStock.objects.get(name=obj.drugs_name)
        ad.stock_count = int(obj.purchase_count)+int(ad.stock_count)
        ad.save()
        return re

admin.site.register(DrugPurchase,DrugPurchaseAdmin)
