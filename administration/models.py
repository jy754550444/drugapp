# coding=utf-8
from django.db import models
from django.contrib.auth.models import User, Group,Permission,GroupManager
from django.utils import timezone
from mptt.models import MPTTModel,TreeForeignKey
#from smart_selects.db_fields import ChainedForeignKey




#药品类别
class Category(MPTTModel):
    name = models.CharField(verbose_name=u'药品类别',max_length=50)
    parent = TreeForeignKey('self',verbose_name=u'父类',on_delete=models.CASCADE, null=True, blank=True, related_name='children', db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'药品类别'
        verbose_name_plural = u'药品类别'


#计量单位
class Unit(models.Model):
    name = models.CharField(verbose_name=u'计量名称',max_length=50,)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'计量单位'
        verbose_name_plural = u'计量单位'

# Create your models here.
#药品库存表
class DrugStock(models.Model):
    name = models.CharField(verbose_name=u'药品名称',max_length=50)
    bar_code = models.CharField(verbose_name=u'药品条码',max_length=50,null=True, blank=True,)
    or_code = models.CharField(verbose_name=u'药品二维码',max_length=50,null=True, blank=True,)
    category = models.ForeignKey(Category,verbose_name=u'药品类别', null=True, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit,verbose_name=u'计量单位', null=True, on_delete=models.CASCADE)
    model = models.CharField(verbose_name=u'规格型号',max_length=50,)
    help_word = models.CharField(verbose_name=u'助记码',max_length=50,null=True, blank=True,)
    manufacturer= models.CharField(verbose_name=u'生产厂家',max_length=50,)
    register_code = models.CharField(verbose_name=u'登记证号',max_length=50,)
    group = models.ForeignKey(Group,verbose_name=u'单位编码', null=True, on_delete=models.CASCADE)
    input_owner = models.ForeignKey(User,verbose_name=u'录入人员', null=True, on_delete=models.CASCADE)
    stock_count=models.IntegerField(verbose_name=u'库存数量',null=True, blank=True,default=0)
    update_time = models.DateTimeField(verbose_name=u'更新时间',auto_now=True,auto_now_add=False)
    create_time = models.DateTimeField(verbose_name=u'录入时间', auto_now_add=True,auto_now=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'药品库存'
        verbose_name_plural = u'药品库存'




#地区
class Region(models.Model):
    name = models.CharField(verbose_name=u'地区名称',max_length=50,)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'地区'
        verbose_name_plural = u'地区'



#药品销售
class DrugSale(models.Model):
    drugs_name = models.ForeignKey(DrugStock,verbose_name=u'药品名称',null=True, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit,verbose_name=u'计量单位', null=True, on_delete=models.CASCADE)
    model = models.CharField(verbose_name=u'规格型号',max_length=50,)
    manufacturer= models.CharField(verbose_name=u'生产厂家',max_length=50,)
    register_code = models.CharField(verbose_name=u'登记证号',max_length=50,)
    customer_name = models.CharField(verbose_name=u'客户姓名',max_length=50,)
    customer_tel = models.CharField(verbose_name=u'客户电话',null=True,blank=True,max_length=50,)
    customer_address = models.CharField(verbose_name=u'客户地址',null=True,blank=True,max_length=50,)
    group = models.ForeignKey(Group,verbose_name=u'单位编码', null=True, on_delete=models.CASCADE)
    input_owner = models.ForeignKey(User,verbose_name=u'录入人员', null=True, on_delete=models.CASCADE)
    sale_count=models.IntegerField(verbose_name=u'销售数量',default=0)
    update_time = models.DateField(verbose_name=u'销售时间',default=timezone.now)
    create_time = models.DateTimeField(verbose_name=u'录入时间', auto_now_add=True,auto_now=False)
    retreat = models.BooleanField(verbose_name=u'退货',default=False)
    retrea_count = models.IntegerField(verbose_name=u'退货数量',default=0)

    def __str__(self):
        return self.drugs_name.name

    class Meta:
        verbose_name = u'药品销售'
        verbose_name_plural = u'药品销售'



#药品采购
class DrugPurchase(models.Model):
    drugs_name = models.ForeignKey(DrugStock,verbose_name=u'药品名称',null=True, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit,verbose_name=u'计量单位', null=True, on_delete=models.CASCADE)
    model = models.CharField(verbose_name=u'规格型号',max_length=50,)
    manufacturer= models.CharField(verbose_name=u'生产厂家',max_length=50,)
    register_code = models.CharField(verbose_name=u'登记证号',max_length=50,)
    group = models.ForeignKey(Group,verbose_name=u'单位编码', null=True, on_delete=models.CASCADE)
    input_owner = models.ForeignKey(User,verbose_name=u'录入人员', null=True, on_delete=models.CASCADE)
    purchase_count= models.IntegerField(verbose_name=u'采购数量')
    update_time = models.DateField(verbose_name=u'采购时间',default=timezone.now)
    create_time = models.DateTimeField(verbose_name=u'录入时间', auto_now_add=True,auto_now=False)
    retreat = models.BooleanField(verbose_name=u'退货',default=False)
    retrea_count = models.IntegerField(verbose_name=u'退货数量',default=0)

    def __str__(self):
        return self.drugs_name.name

    class Meta:
        verbose_name = u'药品采购'
        verbose_name_plural = u'药品采购'