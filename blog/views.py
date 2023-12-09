from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Article
from django.core.cache import cache
from .forms import ArticleForm


@login_required
def create_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            # set author
            article = form.save(commit=False)
            article.author = request.user
            form.save()
            cache.set(f'article_{article.pk}', article, timeout=300)
            return redirect('blog:article_detail', pk=article.pk)
    else:
        form = ArticleForm()

    return_data = {
        'form': form
    }
    return render(request, 'article_form.html', return_data)


@login_required
def update_article(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            cache.set(f'article_{pk}', article, timeout=300)
            return redirect('blog:article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)

    return_data = {
        'form': form
    }
    return render(request, 'article_form.html', return_data)


def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})


def article_detail(request, pk):
    article = cache.get(f'article_{pk}')
    views_key = f'article_views_{pk}'
    views = cache.get(views_key, 0)
    cache.set(views_key, views + 1, timeout=None)
    if not article:
        article = Article.objects.get(pk=pk)
        cache.set(f'article_{pk}', article, timeout=300)

    return_data = {
        'article': article,
        'views': views
    }

    return render(request, 'article_detail.html', return_data)
