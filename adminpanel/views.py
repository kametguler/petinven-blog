from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, FormView, UpdateView, CreateView, ListView
from adminpanel.dashboard_queries import dashboard_queries
from .forms import AuthorProfileForm, PostForm, CategoryForm, TagForm, UserRegisterForm
from blog.models import Author, Post, Category, Tag
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


class DashBoard(TemplateView):
    template_name = 'adminpanel/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dashboard_queries())
        return context


class AuthorProfile(FormView, UpdateView):
    model = Author
    template_name = "adminpanel/pages/author_profile/author_profile.html"
    form_class = AuthorProfileForm
    success_url = "/admin-panel/profile/"

    def get_success_url(self):
        messages.success(self.request, 'Yazar profiliniz başarıyla güncellenmiştir.')
        return super(AuthorProfile, self).get_success_url()

    def get_object(self, queryset=None):
        return self.model.objects.get(user=self.request.user)

    def get_initial(self):
        author = self.get_object()
        initial_values = {"about": author.about,
                          "website": author.website,
                          'profile_photo': author.profile_photo,
                          "facebook": author.facebook,
                          "instagram": author.instagram,
                          "youtube": author.youtube,
                          "linkedin": author.linkedin,
                          "twitter": author.twitter,
                          }
        return initial_values

    def form_valid(self, form):
        if form.is_valid():
            author = form.save(commit=False)
            author.user = self.request.user
            author.save()
            return super(AuthorProfile, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Lütfen form\'u doldurulması gerektiği gibi doldurun!', 'danger')
        return super(AuthorProfile, self).form_invalid(form)


class CreatePostView(CreateView):
    form_class = PostForm
    template_name = 'adminpanel/pages/post/new_post.html'

    def get_success_url(self):
        messages.success(self.request, "Post başarıyla eklendi.")
        succes_url = reverse('adminpanel:create-post')
        return succes_url

    def form_valid(self, form):
        print('sa')
        if form.is_valid():
            post = form.save(commit=False)
            post.title = form.cleaned_data.get('title').title()
            post.author = Author.objects.get(user=self.request.user)
            post.save()
            return super(CreatePostView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors, 'danger')
        return super(CreatePostView, self).form_invalid(form)


class PostListView(ListView):
    model = Post
    template_name = 'adminpanel/pages/post/posts_list.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = super(PostListView, self).get_queryset().filter(author__user=self.request.user)
        status = self.request.GET.get('status', None)

        if status is not None:
            if status == 'taslak':
                queryset = queryset.filter(status=0, author__user=self.request.user)
            if status == 'yayinda':
                queryset = queryset.filter(status=1, author__user=self.request.user)

        return queryset.distinct()


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'adminpanel/pages/post/post_edit.html'
    form_class = PostForm

    def get_success_url(self):
        messages.success(self.request, "Post başarıyla güncellendi.")
        succes_url = reverse('adminpanel:edit-post', kwargs={"slug": self.kwargs.get('slug', None)})
        return succes_url

    def get_object(self, queryset=None):
        obj = get_object_or_404(Post.objects.filter(slug=self.kwargs.get('slug', None), author__user=self.request.user))
        return obj

    def form_invalid(self, form):
        messages.error(self.request, form.errors, 'danger')
        return super(PostUpdateView, self).form_invalid(form)


class CategoryListView(ListView):
    model = Category
    template_name = 'adminpanel/pages/category/category_list.html'


class CreateCategoryView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'adminpanel/pages/category/new_category.html'

    def get_success_url(self):
        messages.success(self.request, "Kategori başarıyla oluşturuldu")
        succes_url = reverse('adminpanel:create-category')
        return succes_url

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super(CreateCategoryView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors, 'danger')
        return super(CreateCategoryView, self).form_invalid(form)


class TagListView(ListView):
    model = Tag
    template_name = 'adminpanel/pages/tag/tag_list.html'


class CreateTagView(CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'adminpanel/pages/tag/new_tag.html'

    def get_success_url(self):
        messages.success(self.request, "Etiket başarıyla oluşturuldu")
        succes_url = reverse('adminpanel:create-tag')
        return succes_url

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super(CreateTagView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors, 'danger')
        return super(CreateTagView, self).form_invalid(form)


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'adminpanel/account/register.html'

    def get_success_url(self):
        messages.success(self.request,
                         "Başarıyla kayıt oldunuz. Admin tarafından yazarlığınız onaylandıktan sonra giriş yapabilirsiniz.")
        succes_url = reverse('adminpanel:register')
        return succes_url

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('email')
            form.save()
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors, 'danger')
        return super(RegisterView, self).form_invalid(form)


class AuthorLoginView(LoginView):
    template_name = "adminpanel/account/login.html"

    def form_valid(self, form):
        qs = Author.objects.filter(user__email=form.cleaned_data.get('username'))
        if qs.exists():
            print(qs.last().is_active)
            if qs.last().is_active:
                return super(AuthorLoginView, self).form_valid(form)
        messages.error(self.request, "Yazarlığınız aktif değil!", 'danger')
        return super(AuthorLoginView, self).form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Bu bilgilere ait kullanıcı bulunamadı", 'danger')
        return super(AuthorLoginView, self).form_invalid(form)
