from django.contrib import admin
from .models import Author, Post, Category, Tag, NewsletterSubscription, HitCount


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_at')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}


class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active')
    search_fields = ['email']


class HitCountAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'post')
    search_fields = ['ip_address']


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author)
admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)
admin.site.register(HitCount, HitCountAdmin)
