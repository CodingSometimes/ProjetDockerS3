from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Article CRU(D)
    path('article/create/', views.create_article, name='create_article'),
    path('', views.article_list, name='blog_index'),
    path('article/<uuid:pk>/', views.article_detail, name='article_detail'),
    path('article/update/<uuid:pk>/', views.update_article, name='update_article'),
]
