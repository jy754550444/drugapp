#-*-coding:utf-8-*-
__author__ = 'malxin'

from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination

class LimitPagination(LimitOffsetPagination):

    default_limit = 20
    limit_query_param = 'rows'
    offset_query_param = 'page'
    max_limit = 100

class PagePagination(PageNumberPagination):

    page_size = 20

    page_query_param = 'page'

    page_size_query_param = 'rows'

    max_page_size = None