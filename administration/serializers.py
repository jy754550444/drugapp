#-*-coding:utf-8-*-
from rest_framework import serializers

__author__ = 'malxin'

from django.contrib.auth.models import Group
from rest_framework.serializers import ModelSerializer


from .models import (
    Category,
    DrugStock,
    Unit,
    DrugPurchase,
    DrugSale
)

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'name',
        ]


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


class DrugStockListSerializer(ModelSerializer):
    category = serializers.CharField(source='category.name',read_only=True)
    units = serializers.CharField(source='unit.name',read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)

    class Meta:
        model = DrugStock
        fields = [
            'id',
            'name',
            'category',
            'units',
            'model',
            'manufacturer',
            'register_code',
            'group_name',
            'stock_count',
        ]



class DrugPurchaseListSerializer(ModelSerializer):
    drugname = serializers.CharField(source='drugs_name.name',read_only=True)
    category = serializers.CharField(source='drugs_name.category.name',read_only=True)
    units = serializers.CharField(source='unit.name',read_only=True)
    group_name = serializers.CharField(source='group.name',read_only=True)

    class Meta:
        model = DrugPurchase
        fields = [
            'drugname',
            'category',
            'units',
            'model',
            'manufacturer',
            'update_time',
            'register_code',
            'group_name',
            'purchase_count',

        ]


class DrugSaleListSerializer(ModelSerializer):
    drugname = serializers.CharField(source='drugs_name.name', read_only=True)
    category = serializers.CharField(source='drugs_name.category.name', read_only=True)
    units = serializers.CharField(source='unit.name', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)

    class Meta:
        model = DrugSale
        fields = [
            'drugname',
            'category',
            'units',
            'model',
            'manufacturer',
            'update_time',
            'register_code',
            'group_name',
            'sale_count',
            'customer_name',
            'customer_tel'
        ]



