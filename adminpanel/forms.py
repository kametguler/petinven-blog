from django import forms
from blog.models import Author, Post, Category, Tag
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AuthorProfileForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('about', 'profile_photo', 'website', 'facebook', 'instagram', 'youtube', 'linkedin', 'twitter')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["about"].widget.attrs.update({'class': "form-control"})
        self.fields["website"].widget.attrs.update({'class': "form-control"})
        self.fields["facebook"].widget.attrs.update({'class': "form-control"})
        self.fields["instagram"].widget.attrs.update({'class': "form-control"})
        self.fields["youtube"].widget.attrs.update({'class': "form-control"})
        self.fields["linkedin"].widget.attrs.update({'class': "form-control"})
        self.fields["twitter"].widget.attrs.update({'class': "form-control"})


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'tags', 'content', 'description', 'image', 'status',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({'class': "form-control"})
        self.fields["content"].widget.attrs.update({'class': "form-control"})
        self.fields["description"].widget.attrs.update({'class': "form-control",
                                                        "placeholder": "Seo için önemli => 155-160 karakter aralığında olmalı.\nİçerik kısmında hazırladığınız yazınızın özetine uygun olacak şekilde yazınız."})
        self.fields["category"].widget.attrs.update({'class': "custom-select"})
        self.fields["tags"].widget.attrs.update({'class': "custom-select"})
        self.fields["status"].widget.attrs.update({'class': "custom-select"})


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({'class': "form-control"})


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({'class': "form-control"})


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=55, required=True)
    last_name = forms.CharField(max_length=55, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
