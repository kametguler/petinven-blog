from django.shortcuts import render
from blog.sidebar_queries import sidebar_query


def not_found(request, exception):
    return render(request, 'not-found.html', sidebar_query())
