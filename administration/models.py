# coding=utf-8
from django.db import models
from django.contrib.auth.models import User, Group
from mptt.models import MPTTModel,TreeForeignKey
#from smart_selects.db_fields import ChainedForeignKey


#药品类别
class Category(MPTTModel):
    drugs_id = models.AutoField(primary_key=True,verbose_name=u'药品编码')
    drugs_name = models.CharField(verbose_name=u'药品名称',max_length=50,)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)


    def __str__(self):
        return self.drugs_name

    class Meta:
        verbose_name = u'药品类别'
        verbose_name_plural = u'药品类别'


#计量单位
class Measurement(models.Model):
    measurement_id = models.AutoField(primary_key=True,verbose_name=u'计量编码')
    metering_name = models.CharField(verbose_name=u'计量名称',max_length=50,)
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)

    def __str__(self):
        return self.metering_name

    class Meta:
        verbose_name = u'计量单位'
        verbose_name_plural = u'计量单位'


# Create your models here.
#药品管理
class Administrations(models.Model):
    drugs_id = models.AutoField(primary_key=True,verbose_name=u'药品编号')
    drugs_name = models.CharField(verbose_name=u'药品名称',max_length=50)
    bar_code = models.CharField(verbose_name=u'药品条码',max_length=50,null=True, blank=True,)
    or_code = models.CharField(verbose_name=u'药品二维码',max_length=50,null=True, blank=True,)
    category = models.ForeignKey(Category,verbose_name=u'药品类别', null=True, on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurement,verbose_name=u'计量单位', null=True, on_delete=models.CASCADE)
    model = models.CharField(verbose_name=u'规格型号',max_length=50,)
    mnemonic = models.CharField(verbose_name=u'助记码',max_length=50,null=True, blank=True,)
    manufacturer= models.CharField(verbose_name=u'生产厂家',max_length=50,)
    register_code = models.CharField(verbose_name=u'登记证号',max_length=50,)
    company_id = models.ForeignKey(Group,verbose_name=u'单位编码', null=True, on_delete=models.CASCADE)
    input_owner = models.ForeignKey(User,verbose_name=u'录入人员', null=True, on_delete=models.CASCADE)
    stock_count=models.CharField(verbose_name=u'库存数量',max_length=50,null=True, blank=True,)
    update_time = models.DateTimeField(verbose_name=u'更新时间',auto_now=True,auto_now_add=False)
    create_time = models.DateTimeField(verbose_name=u'录入时间', auto_now_add=True,auto_now=False)

    def __str__(self):
        return self.drugs_name

    class Meta:
        verbose_name = u'药品管理'
        verbose_name_plural = u'药品管理'




#地区
class Region(models.Model):
    region_name = models.CharField(verbose_name=u'地区名称',max_length=50,)
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)

    def __str__(self):
        return self.region_name

    class Meta:
        verbose_name = u'地区'
        verbose_name_plural = u'地区'


#药品销售
class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True,verbose_name=u'销售编号')
    drugs_name = models.ForeignKey(Administrations,verbose_name=u'药品名称',null=True, on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurement,verbose_name=u'计量单位', null=True, on_delete=models.CASCADE)
    model = models.CharField(verbose_name=u'规格型号',max_length=50,)
    manufacturer= models.CharField(verbose_name=u'生产厂家',max_length=50,)
    register_code = models.CharField(verbose_name=u'登记证号',max_length=50,)
    customer_name = models.CharField(verbose_name=u'客户姓名',max_length=50,)
    customer_tel = models.CharField(verbose_name=u'客户电话',max_length=50,)
    customer_address = models.CharField(verbose_name=u'客户地址',max_length=50,)
    company_id = models.ForeignKey(Group,verbose_name=u'单位编码', null=True, on_delete=models.CASCADE)
    input_owner = models.ForeignKey(User,verbose_name=u'录入人员', null=True, on_delete=models.CASCADE)
    sale_count=models.CharField(verbose_name=u'销售数量',max_length=50,)
    update_time = models.DateTimeField(verbose_name=u'更新时间',auto_now=True,auto_now_add=False)
    create_time = models.DateTimeField(verbose_name=u'录入时间', auto_now_add=True,auto_now=False)

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = u'药品销售'
        verbose_name_plural = u'药品销售'



#药品采购
class Storage(models.Model):
    storage_id = models.AutoField(primary_key=True,verbose_name=u'采购编号')
    drugs_name = models.ForeignKey(Administrations,verbose_name=u'药品名称',null=True, on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurement,verbose_name=u'计量单位', null=True, on_delete=models.CASCADE)
    model = models.CharField(verbose_name=u'规格型号',max_length=50,)
    manufacturer= models.CharField(verbose_name=u'生产厂家',max_length=50,)
    register_code = models.CharField(verbose_name=u'登记证号',max_length=50,)
    company_id = models.ForeignKey(Group,verbose_name=u'单位编码', null=True, on_delete=models.CASCADE)
    input_owner = models.ForeignKey(User,verbose_name=u'录入人员', null=True, on_delete=models.CASCADE)
    stock_count=models.CharField(verbose_name=u'采购数量',max_length=50,)
    update_time = models.DateTimeField(verbose_name=u'更新时间', auto_now=True,auto_now_add=False)
    create_time = models.DateTimeField(verbose_name=u'录入时间', auto_now_add=True,auto_now=False)

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = u'药品采购'
        verbose_name_plural = u'药品采购'