from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, UpdateView
from .models import Post, NewsletterSubscription, HitCount
from .sidebar_queries import sidebar_query
from meta.views import Meta
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.views.generic.edit import FormView
from .forms import ContactForm, EmailSubscriptionForm
from django.contrib import messages
from django.shortcuts import redirect


class HomePage(ListView):
    queryset = Post.objects.filter(status=1)
    model = Post
    template_name = 'index.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super(HomePage, self).get_queryset()
        search = self.request.GET.get('search', None)
        tag = self.request.GET.get('tag', None)
        category = self.request.GET.get('category', None)
        author = self.request.GET.get('author', None)
        queryset = queryset.annotate(
            full_name=Concat('author__user__first_name', V(' '), 'author__user__last_name'))
        if search is not None:
            if search != "":
                queryset = queryset.filter(
                    Q(title__icontains=search) | Q(tags__name__icontains=search) | Q(content__icontains=search) | Q(
                        full_name__icontains=search))
        if tag is not None:
            if tag != "":
                queryset = queryset.filter(tags__slug=tag)

        if category is not None:
            if category != "":
                queryset = queryset.filter(category__slug=category)

        if author is not None:
            if author != "":
                queryset = queryset.filter(full_name=author)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        meta = Meta(
            title="Petinven - Anasayfa",
            description='Blog sayfası',
        )
        context["meta"] = meta
        context.update(sidebar_query())
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'

    def get_client_ip(self, *args, **kwargs):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_object(self, queryset=None):
        obj = super(PostDetailView, self).get_object()
        HitCount.objects.get_or_create(post=obj, ip_address=self.get_client_ip())
        return obj

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['meta'] = self.get_object().as_meta(self.request)
        context.update(sidebar_query(self.object.category, self.object.id))
        return context


class ContactUsView(FormView):
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = '/iletisim/'

    def form_valid(self, form):
        if form.send_email():
            messages.success(self.request, 'İletiniz başarıyla gönderilmiştir')

        return super(ContactUsView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ContactUsView, self).get_context_data(**kwargs)
        meta = Meta(
            title="Petinven - İletişim",
            description='Petinven iletişim. Yazarımız mı olmak istiyorsun? Bizimle iletişime geç.',
        )
        context["meta"] = meta
        context.update(sidebar_query())

        return context


class EmailSubscriptionView(FormView):
    form_class = EmailSubscriptionForm
    template_name = 'index.html'

    def form_valid(self, form):
        if form.is_valid():
            instance = form.save()
            form.send_email(instance)

        return JsonResponse({"message": 'Aboneliğiniz başarıyla aktif edildi!', "class": "alert-success"})

    def form_invalid(self, form):
        email = form.data.get('email')
        qs = NewsletterSubscription.objects.all()
        if qs.filter(email=email, is_active=True).exists():
            return JsonResponse({"message": 'Bu email adresi zaten abone!', "class": "alert-warning"})
        elif qs.filter(email=email, is_active=False).exists():
            qs = qs.filter(email=email, is_active=False).last()
            qs.is_active = True
            qs.save()
            form.send_email(qs)
            return JsonResponse({"message": 'Aboneliğiniz tekrar aktif edildi!', "class": "alert-success"})
        else:
            return JsonResponse({"message": 'Abonelik sırasında hata meydana geldi!', "class": "alert-danger"})


class EmailSubscriptionDeactivateView(UpdateView):
    model = NewsletterSubscription
    fields = ["email", "is_active"]
    slug_field = "email"
    success_url = "/"
    template_name = "email/deactivate_subscription.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
            self.object.save()
        else:
            return redirect('/')
        return super().get(request, *args, **kwargs)
