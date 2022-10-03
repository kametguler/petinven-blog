from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import DashBoard, AuthorProfile, CreatePostView, PostListView, PostUpdateView, CategoryListView, \
    CreateCategoryView, TagListView, CreateTagView, RegisterView, AuthorLoginView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(DashBoard.as_view()), name='dashboard'),
    path('profile/', login_required(AuthorProfile.as_view()), name='profile'),
    path('post/new-post/', login_required(CreatePostView.as_view()), name='create-post'),
    path('post/list/', login_required(PostListView.as_view()), name='list-post'),
    path('post/<slug:slug>/', login_required(PostUpdateView.as_view()), name='edit-post'),
    path('category/list/', login_required(CategoryListView.as_view()), name='list-category'),
    path('category/create/', login_required(CreateCategoryView.as_view()), name='create-category'),
    path('tag/list/', login_required(TagListView.as_view()), name='list-tag'),
    path('tag/create/', login_required(CreateTagView.as_view()), name='create-tag'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', AuthorLoginView.as_view(template_name='adminpanel/account/login.html', ), name='login'),
    path('logout/', LogoutView.as_view(template_name='adminpanel/account/logout.html', ), name='logout'),
]
