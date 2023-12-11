from django.urls import path, register_converter
from . import views

app_name = 'blog'


class BooleanConverter:
    regex = 'True|False'

    def to_python(self, value):
        return value == 'True'

    def to_url(self, value):
        return str(value)


register_converter(BooleanConverter, "bool")

urlpatterns = [
    # Article CRU(D)
    path('article/create/', views.create_article, name='create_article'),
    path('', views.article_list, name='blog_index'),
    path('article/<uuid:pk>/', views.article_detail, name='article_detail'),
    path(
        'article/<uuid:pk>/<bool:incr_views>/', views.article_detail, name='article_detail_from_comment'
    ),
    path('article/update/<uuid:pk>/', views.update_article, name='update_article'),
]
