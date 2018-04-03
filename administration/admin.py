# coding=utf-8

import mptt
from django.db import models
from mptt.fields import TreeForeignKey
from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import DrugStock,Category,Unit,Region,DrugSale,DrugPurchase

from mptt.admin import MPTTModelAdmin
# Register your models here.



#add a parent foreign key
TreeForeignKey(Group, blank=True, null=True,verbose_name='父类',on_delete=models.CASCADE, db_index=True).contribute_to_class(Group, 'parent')
mptt.register(Group, order_insertion_by=['name'])

#药品库存

class DrugStockAdmin(admin.ModelAdmin):
    list_display = [ 'name','category','unit', 'model', 'manufacturer','register_code', 'stock_count' ]
    fields = ('name', 'bar_code', 'or_code', 'category', 'unit', 'model', 'manufacturer','register_code','stock_count',)
    search_fields = ('name','category__name','model','manufacturer','register_code')
    list_filter = ('category','create_time')

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


    def get_queryset(self, request):
        qs = super(CategoryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)


#计量单位
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

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
    list_display = ['drugs_name','unit','model','manufacturer','register_code','customer_name','customer_tel','sale_count', 'update_time','retrea_count' ]
    fields = ('drugs_name', 'unit', 'model', 'manufacturer', 'register_code', 'customer_name', 'customer_tel',
              'customer_address', 'sale_count','update_time','retreat','retrea_count')
    search_fields = ['drugs_name__name','customer_name','customer_tel','model','manufacturer','register_code']
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
        ds = DrugStock.objects.get(id=obj.drugs_name.id)
        if change:
            if obj.retreat == True:
                if obj.sale_count >=obj.retrea_count:
                    ds.stock_count = obj.retrea_count+ds.stock_count
                    obj.sale_count = obj.sale_count-obj.retrea_count
                    obj.retrea_count = obj.retrea_count
                    ds.save()
                    obj.save()
                else:
                    # print("退货大于库存量，不能退货")
                    return not change
            else:
                return not change
        else:
            if ds.stock_count > obj.sale_count:
                ds.stock_count = ds.stock_count - obj.sale_count
                ds.save()
        obj.input_owner = request.user
        userobj = request.user
        if userobj.groups.count() > 0:
            groups = userobj.groups.all()
            group = Group.objects.get(pk=groups[0].id)
            obj.group = group
        obj.save()
admin.site.register(DrugSale, DrugSaleAdmin)

#采购
class DrugPurchaseAdmin(admin.ModelAdmin):
    list_display = ('drugs_name','unit','model','manufacturer','register_code','purchase_count','update_time','retrea_count')
    fields  = ('drugs_name','unit','model','manufacturer','register_code','purchase_count','update_time','retreat','retrea_count')
    search_fields = ['drugs_name__name','model','manufacturer','register_code']
    list_filter = ('update_time',)

    def get_queryset(self, request):
        qs = super(DrugPurchaseAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            groups = request.user.groups.all()
            group = Group.objects.get(pk=groups[0].id)
            return qs.filter(group=group)

    def save_model(self, request, obj, form, change):
        ad = DrugStock.objects.get(id = obj.drugs_name.id)
        if change:
            if obj.retreat == True:
                if obj.purchase_count < obj.retrea_count:
                    # print("退货大于库存量，不能退货")
                    return not change
                else:
                    ad.stock_count = ad.stock_count-obj.retrea_count
                    obj.purchase_count = obj.purchase_count-obj.retrea_count
                    obj.retrea_count = obj.retrea_count
                    ad.save()
                    obj.save()
            else:
                return not change
        else:
            ad.stock_count = obj.purchase_count + ad.stock_count
            ad.save()

        obj.input_owner = request.user
        userobj = request.user
        if userobj.groups.count() > 0:
            groups = userobj.groups.all()
            group = Group.objects.get(pk=groups[0].id)
            obj.group = group
        obj.save()
        return obj
admin.site.register(DrugPurchase,DrugPurchaseAdmin)
