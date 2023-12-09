from django.contrib import admin
from .models import Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    ordering = ('created_at',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('content',)
    date_hierarchy = 'created_at'
    ordering = ('created_at',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
