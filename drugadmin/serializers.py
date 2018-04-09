#-*-coding:utf-8-*-
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from administration.models import Unit, Category, DrugSale, DrugStock, DrugPurchase
from .models import SaleReturn, PurchaseReturn

__author__ = 'malxin'



class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'parent',
        ]



class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = [
            'id',
            'name',
        ]


class DrugStockSerializer(ModelSerializer):
    categoryname = serializers.CharField(source='category.name',read_only=True)
    unitname = serializers.CharField(source='unit.name',read_only=True)

    class Meta:
        model = DrugStock
        fields = [
            'id',
            'name',
            'category',
            'categoryname',
            'unit',
            'unitname',
            'model',
            'manufacturer',
            'register_code',
            'stock_count',
        ]


class DrugStockListSerializer(ModelSerializer):
    categoryname = serializers.CharField(source='category.name',read_only=True)
    unitname = serializers.CharField(source='unit.name',read_only=True)

    class Meta:
        model = DrugStock
        fields = [
            'id',
            'name',
            'category',
            'categoryname',
            'unit',
            'unitname',
            'model',
            'manufacturer',
            'register_code',
            'bar_code',
            'or_code',
            'stock_count',
        ]



class DrugSaleSerializer(ModelSerializer):
    unitname = serializers.CharField(source='unit.name', read_only=True)
    drugname = serializers.CharField(source='drugs_name.name', read_only=True)
    class Meta:
        model = DrugSale
        fields = [
            'id',
            'drugs_name',
            'drugname',
            'unit',
            'unitname',
            'model',
            'manufacturer',
            'register_code',
            'customer_name',
            'customer_tel',
            'customer_address',
            'sale_count',
            'update_time',
        ]


class DrugPurchaseSerializer(ModelSerializer):
    drugname = serializers.CharField(source='drugs_name.name',read_only=True)
    unitname = serializers.CharField(source='unit.name',read_only=True)

    class Meta:
        model = DrugPurchase
        fields = [
            'id',
            'drugs_name',
            'drugname',
            'unit',
            'unitname',
            'model',
            'manufacturer',
            'update_time',
            'register_code',
            'purchase_count',

        ]

class PurSearchSerializer(ModelSerializer):
    drugname = serializers.CharField(source='drugs_name.name',read_only=True)
    unitname = serializers.CharField(source='unit.name',read_only=True)
    categoryname = serializers.CharField(source='drugs_name.category.name',read_only=True)

    class Meta:
        model = DrugPurchase
        fields = [
            'id',
            #'drugs_name',
            'drugname',
            'categoryname',
            #'unit',
            'unitname',
            'model',
            'manufacturer',
            'update_time',
            'register_code',
            'purchase_count',

        ]

class SaleSearchSerializer(ModelSerializer):
    unitname = serializers.CharField(source='unit.name', read_only=True)
    drugname = serializers.CharField(source='drugs_name.name', read_only=True)
    categoryname = serializers.CharField(source='drugs_name.category.name', read_only=True)
    class Meta:
        model = DrugSale
        fields = [
            'id',
            'drugname',
            'categoryname',
            'unitname',
            'model',
            'manufacturer',
            'register_code',
            'customer_name',
            'customer_tel',
            'customer_address',
            'sale_count',
            'update_time',
        ]

class SaleReturnSerializer(ModelSerializer):
    unitname = serializers.CharField(source='unit.name', read_only=True)
    drugname = serializers.CharField(source='name.name', read_only=True)
    class Meta:
        model = SaleReturn
        fields = [
            'id',
            'name',
            'drugname',
            'unit',
            'unitname',
            'model',
            'manufacturer',
            'register_code',
            'return_count',
            'return_at',
        ]

class PurchaseReturnSerializer(ModelSerializer):
    unitname = serializers.CharField(source='unit.name', read_only=True)
    drugname = serializers.CharField(source='name.name', read_only=True)
    class Meta:
        model = PurchaseReturn
        fields = [
            'id',
            'name',
            'drugname',
            'unit',
            'unitname',
            'model',
            'manufacturer',
            'register_code',
            'return_count',
            'return_at',
        ]