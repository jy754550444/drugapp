#-*-coding:utf-8-*-
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from .views import (
    index,
    userlogin,
    SaleListAPIView,
    SaleCreateAPIView,
    SaleUpdateAPIView,
    SaleDeleteAPIView,
    UnitListAPIView,
    CompanyStockListAPIView,
    userlogout,
    CategoryListAPIView,
    CategoryTreeListAPIView,
    StockDetailAPIView,
    purchase,
    PurchaseListAPIView,
    PurchaseCreateAPIView,
    changepwd,
    stock,
    StockListAPIView,
    StockCreateAPIView,
    StockDeleteAPIView,
    pursearch,
    PurSearchAPIView,
    SaleSearchAPIView,
    salesearch,
    stocksearch,
    StockSearchAPIView,
    purreturn,
    salereturn,
    PurReturnListAPIView,
    PurReturnCreateAPIView,
    SaleReturnListAPIView,
    SaleReturnCreateAPIView,
    lefttree,
)

__author__ = 'malxin'


urlpatterns = [
    url(r'^$', userlogin , name="drugadmin-login"),
    url(r'^index/$', index, name="drugadmin-index"),
    url(r'^changepwd/$', changepwd, name="drugadmin-changepwd"),
    url(r'^logout/$', userlogout, name="drugadmin-logout"),
    url(r'^unitlist/$', UnitListAPIView.as_view(), name="drug-unit-list"),
    url(r'^itemlist/$', CompanyStockListAPIView.as_view(), name="drug-item-list"),
    url(r'^catelist/$', CategoryListAPIView.as_view(), name="drug-category-list"),
    url(r'^clist/$', CategoryTreeListAPIView.as_view(), name="drug-cate-list"),
    url(r'^treelist/$', lefttree, name="drug-tree-list"),

    #sale action
    url(r'^salelist/$', SaleListAPIView.as_view(), name="drug-sale-list"),
    url(r'^salesave/$', SaleCreateAPIView.as_view(), name="drug-sale-save"),
    url(r'^saleupdate/$', SaleUpdateAPIView.as_view(), name="drug-sale-update"),
    url(r'^saledelete/$', SaleDeleteAPIView.as_view(), name="drug-sale-delete"),
    url(r'^salesearch/$', salesearch, name="drugadmin-salesearch"),
    url(r'^salesearchlist/$', SaleSearchAPIView.as_view(), name="drug-sale-search"),
    url(r'^salereturn/$', salereturn, name="drugadmin-salereturn"),


    #stock
    url(r'^stockitem/(?P<pk>\d+)/$', StockDetailAPIView.as_view(), name="drug-stock-item"),
    url(r'^stock/$', stock, name="drugadmin-stock"),
    url(r'^stocklist/$', StockListAPIView.as_view(), name="drug-stock-list"),
    url(r'^stocksave/$', StockCreateAPIView.as_view(), name="drug-stock-save"),
    url(r'^stockdelete/$', StockDeleteAPIView.as_view(), name="drug-stock-del"),
    url(r'^stocksearch/$', stocksearch, name="drugadmin-stocksearch"),
    url(r'^stocksearchlist/$', StockSearchAPIView.as_view(), name="drug-stock-search"),

    #purchase
    url(r'^purchase/$', purchase, name="drugadmin-phurchase"),
    url(r'^purchaselist/$', PurchaseListAPIView.as_view(), name="drug-purchase-list"),
    url(r'^purchasesave/$', PurchaseCreateAPIView.as_view(), name="drug-purchase-save"),
    url(r'^pursearch/$', pursearch, name="drugadmin-pursearch"),
    url(r'^pursearchlist/$', PurSearchAPIView.as_view(), name="drug-purchase-search"),
    #采购退货
    url(r'^purreturn/$', purreturn, name="drugadmin-purreturn"),
    url(r'^purreturnlist/$', PurReturnListAPIView.as_view(), name="drug-purreturn-list"),
    url(r'^purreturnsave/$', PurReturnCreateAPIView.as_view(), name="drug-purreturn-save"),
    url(r'^salereturn/$', salereturn, name="drugadmin-salereturn"),
    url(r'^salereturnlist/$', SaleReturnListAPIView.as_view(), name="drug-salereturn-list"),
    url(r'^salereturnsave/$', SaleReturnCreateAPIView.as_view(), name="drug-salereturn-save"),
]
