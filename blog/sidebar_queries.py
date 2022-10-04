from .models import Post, Category
from django.db.models import Count


def sidebar_query(category=None, id=None):
    context = {}
    context['recent_posts'] = Post.objects.filter(status=1).order_by('-id')[:3]
    categories = Category.objects.all().annotate(posts_count=Count('blog_posts'))
    context['popular_categories'] = categories.filter().order_by('-posts_count')[:7]
    context['popular_posts'] = sorted(Post.objects.filter(status=1), key=lambda a: a.get_hit_count, reverse=True)[:3]

    if category is not None:
        also_like = Post.objects.filter(status=1, category=category).order_by('-id').exclude(id=id)[:2]
        if also_like.count() == 0:
            also_like = Post.objects.filter(status=1).order_by('-id').exclude(id=id)[:2]
        context['also_like'] = also_like

    return context
