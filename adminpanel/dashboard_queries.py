from blog.models import Post, Author, Category, Tag


def dashboard_queries():
    context = {}
    context['posts_count'] = Post.objects.filter(status=1).count()
    context['authors_count'] = Author.objects.filter().count()
    context['categories_count'] = Category.objects.all().count()
    context['tags_count'] = Tag.objects.filter().count()
    return context
