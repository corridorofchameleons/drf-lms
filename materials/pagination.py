from rest_framework.pagination import PageNumberPagination


class MyPaginator(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    max_page_size = 20
