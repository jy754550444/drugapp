# coding=utf-8
from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Administrations,Category,Measurement,Region,Sale,Storage

from mptt.admin import MPTTModelAdmin
# Register your models here.

#药品管理
class AdministrationsAdmin(admin.ModelAdmin):
    list_display = ['drugs_id', 'drugs_name', 'stock_count','company_id','input_owner', 'update_time', 'create_time', ]
    fields = ('drugs_name', 'bar_code', 'or_code', 'category', 'measurement', 'model', 'mnemonic', 'manufacturer',
              'register_code', 'stock_count',)
    search_fields = ('drugs_id',)
    list_filter = ('drugs_name',)

    def save_model(self, request, obj, form, change):
        obj.input_owner = request.user
        userobj = request.user
        if userobj.groups.count() > 0:
            groups = userobj.groups.all()
            group = Group.objects.get(pk=groups[0].id)
            obj.company_id = group
        obj.save()

    def get_queryset(self, request):
        qs = super(AdministrationsAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            groups = request.user.groups.all()
            group = Group.objects.get(pk=groups[0].id)
            return qs.filter(company_id=group)

admin.site.register(Administrations, AdministrationsAdmin)

#药品类别
class CategoryAdmin(MPTTModelAdmin):
    # list_display = ['drugs_id', 'drugs_name','parent','create_time',]
    # fields  = ('project','title','content','category','uploadfile')
    search_fields = ['drugs_id']
    list_filter = ('drugs_name',)

    def get_queryset(self, request):
        qs = super(CategoryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)

admin.site.register(Category, CategoryAdmin)


#计量单位
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ['measurement_id', 'metering_name','create_time',]
    # fields  = ('project','title','content','category','uploadfile')
    search_fields = ['measurement_id']
    list_filter = ('metering_name',)


    def get_queryset(self, request):
        qs = super(MeasurementAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)
admin.site.register(Measurement,MeasurementAdmin)


#地区
class RegionAdmin(admin.ModelAdmin):
    list_display = ['region_name','create_time',]
    # fields  = ('project','title','content','category','uploadfile')
    search_fields = ['region_name']
    list_filter = ('region_name',)



    def get_queryset(self, request):
        qs = super(RegionAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:

            return qs.filter(user=request.user)
admin.site.register(Region,RegionAdmin)


#药品销售
class SaleAdmin(admin.ModelAdmin):
    list_display = ['sale_id', 'drugs_name', 'sale_count', 'update_time', 'create_time', ]
    fields = ('drugs_name', 'measurement', 'model', 'manufacturer', 'register_code', 'customer_name', 'customer_tel',
              'customer_address', 'sale_count')
    search_fields = ['sale_id']
    list_filter = ('drugs_name',)



    def get_queryset(self, request):
        qs = super(SaleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            groups = request.user.groups.all()
            group = Group.objects.get(pk=groups[0].id)
            return qs.filter(company_id=group)

    def save_model(self, request, obj, form, change):

        ad = Administrations.objects.get(drugs_name=obj.drugs_name)
        if int(ad.stock_count)>int(obj.sale_count):
            ad.stock_count = int(ad.stock_count)-int(obj.sale_count)
            ad.save()
            re = super(SaleAdmin,self).save_model(request, obj, form, change)
            return re


        obj.input_owner = request.user
        userobj = request.user
        if userobj.groups.count() > 0:
            groups = userobj.groups.all()
            group = Group.objects.get(pk=groups[0].id)
            obj.company_id = group
        obj.save()
admin.site.register(Sale, SaleAdmin)


class StorageAdmin(admin.ModelAdmin):
    list_display = ('storage_id','drugs_name','stock_count','update_time','create_time')
    fields  = ('drugs_name','measurement','model','manufacturer','register_code','stock_count')
    search_fields = ['storage_id']
    list_filter = ('drugs_name',)

    def get_queryset(self, request):
        qs = super(StorageAdmin, self).get_queryset(request)
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

        re = super(StorageAdmin,self).save_model(request, obj, form, change)
        ad = Administrations.objects.get(drugs_name=obj.drugs_name)
        ad.stock_count = int(obj.stock_count)+int(ad.stock_count)
        ad.save()
        return re



admin.site.register(Storage,StorageAdmin)
