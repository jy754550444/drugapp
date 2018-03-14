# coding=utf-8
"""worklog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from administration.views import userlogin, CheckCode, admins, index, stock_list, sale_list, purchase_list, \
    DrugStockListView, sale_count, purchase_count,stock_count,DrugPurchaseListView,DrugSaleListView, userlogout,changepwd

admin.site.site_header = u'农药追溯系统'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^chaining/',include('smart_selects.urls')),
    url(r'^checkcode/$', CheckCode),
    url(r'^login/$',userlogin , name="drug-login"),
    url(r'^logout/$', userlogout , name="drug-logout"),
    url(r'^changepwd/$', changepwd , name="drug-changepwd"),
    url(r'^admins/$', admins),
    url(r'^index/$', index, name="drug-index"),
    url(r'^stock_list/$', stock_list, name="stock-list"),
    url(r'^sale_count/$', sale_count, name="sale-count"),
    url(r'^sale_list/$', sale_list, name="sale-list"),
    url(r'^purchase_count/$', purchase_count, name="purchase-count"),
    url(r'^stock_count/$', stock_count, name="stock-count"),
    url(r'^purchase_list/$', purchase_list, name="purchase-list"),
    url(r'^api_stocklist/$', DrugStockListView.as_view(), name="api-stocklist"),
    url(r'^api_purchaselist/$', DrugPurchaseListView.as_view(), name="api-purchaselist"),
    url(r'^api_salelist/$', DrugSaleListView.as_view(), name="api-salelist"),
    # url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    # url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLSc
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
