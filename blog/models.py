from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.text import slugify
from meta.models import ModelMeta
from django.conf import settings

STATUS = (
    (0, "Taslak"),
    (1, "Yayında")
)


class NewsletterSubscription(models.Model):
    email = models.EmailField(verbose_name='Email', unique=True)
    is_active = models.BooleanField(default=True, verbose_name='Aktif mi ?')

    class Meta:
        verbose_name = "Bülten Abonesi"
        verbose_name_plural = "Bülten Aboneleri"

    def __str__(self):
        return self.email

    def get_deactivate_url(self):
        return f"{settings.META_SITE_PROTOCOL}://{settings.META_SITE_DOMAIN}{reverse('subscription-deactivate', kwargs={'slug': self.email})}"


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blog_authors')
    about = models.TextField(verbose_name='Hakkında')
    profile_photo = models.ImageField(upload_to='profiles/', default='profiles/avatar.png', null=True, blank=True)
    website = models.URLField(verbose_name='Website Linki', blank=True, null=True)
    facebook = models.URLField(verbose_name='Facebook Linki', blank=True, null=True)
    instagram = models.URLField(verbose_name='Instagram Linki', blank=True, null=True)
    youtube = models.URLField(verbose_name='Youtube Linki', blank=True, null=True)
    linkedin = models.URLField(verbose_name='Linkedin Linki', blank=True, null=True)
    twitter = models.URLField(verbose_name='Twitter Linki', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    is_active = models.BooleanField(default=False, verbose_name='Aktif mi ?')

    class Meta:
        verbose_name = 'Yazar'
        verbose_name_plural = 'Yazarlar'

    def get_profile_image(self):
        if self.profile_photo:
            return self.profile_photo.url

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Kategori', unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'

    def __str__(self):
        return self.title

    def get_unique_slug(self):
        slug = slugify(self.title.replace('ı', 'i'))
        unique_slug = slug
        counter = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{counter}'
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = self.get_unique_slug()
            return super(Category, self).save(*args, **kwargs)
        else:
            return super(Category, self).save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='Etiket', unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    class Meta:
        verbose_name = 'Etiket'
        verbose_name_plural = 'Etiketler'

    def __str__(self):
        return self.name

    def get_unique_slug(self):
        slug = slugify(self.name.replace('ı', 'i'))
        unique_slug = slug
        counter = 1
        while Tag.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{counter}'
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = self.get_unique_slug()
            return super(Tag, self).save(*args, **kwargs)
        else:
            return super(Tag, self).save(*args, **kwargs)


class HitCount(models.Model):
    ip_address = models.GenericIPAddressField()
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Görüntülenme Sayısı"
        verbose_name_plural = "Görüntülenme Sayıları"

    def __str__(self):
        return f'{self.ip_address} => {self.post.title}'


class Post(ModelMeta, models.Model):
    title = models.CharField(max_length=255, verbose_name='Başlık')
    slug = models.SlugField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blog_posts',
                               verbose_name="Yazarı")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blog_posts',
                                 verbose_name="Kategorisi", null=True)
    tags = models.ManyToManyField(Tag, related_name='blog_posts', verbose_name='Etiketler')
    image = models.ImageField(verbose_name='Fotoğraf (800x460)')
    content = RichTextField()
    description = models.TextField(null=True)
    status = models.IntegerField(choices=STATUS, default=0, verbose_name='Yayın Durumu')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Postlar'

    _metadata = {
        'title': 'title',
        'description': 'description',
        'image': 'get_meta_image',
    }

    def get_unique_slug(self):
        slug = slugify(self.title.replace('ı', 'i'))
        unique_slug = slug
        counter = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{counter}'
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = self.get_unique_slug()
            return super(Post, self).save(*args, **kwargs)
        else:
            return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_tweet_intent(self):
        tweet_intent = f"https://twitter.com/intent/tweet?text={self.title}&url={settings.META_SITE_DOMAIN}{self.get_absolute_url()}"
        return tweet_intent

    def get_facebook_intent(self):
        facebook_intent = f"https://facebook.com/sharer.php?u={settings.META_SITE_DOMAIN}{self.get_absolute_url()}"
        return facebook_intent

    def get_meta_image(self):
        if self.image:
            return self.image.url

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    def get_admin_absolute_url(self):
        return reverse('adminpanel:edit-post', kwargs={'slug': self.slug})

    @property
    def get_hit_count(self):
        return HitCount.objects.filter(post=self).count()
