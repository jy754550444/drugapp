# coding=utf-8
from django.contrib.auth.models import User, Group
from django.db import models

# Create your models here.
from django.utils import timezone

from administration.models import DrugStock, Unit


#药品销售退货
class SaleReturn(models.Model):
    name = models.ForeignKey(DrugStock,verbose_name=u'药品名称',null=True, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit,verbose_name=u'计量单位', null=True, on_delete=models.SET_NULL)
    model = models.CharField(verbose_name=u'规格型号',max_length=50,)
    manufacturer= models.CharField(verbose_name=u'生产厂家',max_length=50,)
    register_code = models.CharField(verbose_name=u'登记证号',max_length=50,)
    group = models.ForeignKey(Group,verbose_name=u'单位名称', null=True, on_delete=models.CASCADE)
    input_owner = models.ForeignKey(User,verbose_name=u'录入人员', null=True, on_delete=models.SET_NULL)
    return_count=models.IntegerField(verbose_name=u'退货数量',default=0)
    return_at = models.DateField(verbose_name=u'退货时间',default=timezone.now)
    create_at = models.DateTimeField(verbose_name=u'录入时间', auto_now_add=True,auto_now=False)

    def __str__(self):
        return self.name.name

    class Meta:
        verbose_name = u'销售退货'
        verbose_name_plural = u'销售退货'



#药品采购退货
class PurchaseReturn(models.Model):
    name = models.ForeignKey(DrugStock,verbose_name=u'药品名称',null=True, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit,verbose_name=u'计量单位', null=True, on_delete=models.SET_NULL)
    model = models.CharField(verbose_name=u'规格型号',max_length=50,)
    manufacturer= models.CharField(verbose_name=u'生产厂家',max_length=50,)
    register_code = models.CharField(verbose_name=u'登记证号',max_length=50,)
    group = models.ForeignKey(Group,verbose_name=u'单位名称', null=True, on_delete=models.CASCADE)
    input_owner = models.ForeignKey(User,verbose_name=u'录入人员', null=True, on_delete=models.SET_NULL)
    return_count= models.IntegerField(verbose_name=u'退货数量')
    return_at = models.DateField(verbose_name=u'退货时间',default=timezone.now)
    create_at = models.DateTimeField(verbose_name=u'录入时间', auto_now_add=True,auto_now=False)

    def __str__(self):
        return self.name.name

    class Meta:
        verbose_name = u'采购退货'
        verbose_name_plural = u'药品退货'