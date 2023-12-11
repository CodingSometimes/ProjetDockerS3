from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Article
from django.core.cache import cache
from .forms import ArticleForm, CommentForm


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


def article_detail(request, pk, incr_views=True):
    print("INCR_VIEWS : ", incr_views)
    # Récupération de l'article à afficher
    article = cache.get(f'article_{pk}')
    if not article:
        article = Article.objects.get(pk=pk)
        cache.set(f'article_{pk}', article, timeout=300)

    # Création de commentaires
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.author = request.user
            new_comment.save()

            comments = article.comments.all()
            cache.set(f'comments_for_{pk}', comments, timeout=300)
            return redirect('blog:article_detail_from_comment', pk=pk, incr_views=False)

    # Récupération des commentaires
    comments = cache.get(f'comments_for_{pk}')
    if not comments:
        comments = article.comments.all()
        cache.set(f'comments_for_{pk}', comments, timeout=300)
    for comment in comments:
        comment.likes = cache.get(f'comment_likes_{comment.pk}', 0)
        comment.dislikes = cache.get(f'comment_dislikes_{comment.pk}', 0)

    views_key = f'article_views_{pk}'
    views = cache.get(views_key, 0)
    if incr_views:
        cache.set(views_key, views + 1, timeout=None)
    views = cache.get(views_key)

    return_data = {
        'article': article,
        'views': views,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'article_detail.html', return_data)

