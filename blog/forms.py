from django import forms
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .models import NewsletterSubscription


class ContactForm(forms.Form):
    name = forms.CharField(max_length=55)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    topic = forms.CharField(max_length=255)
    message = forms.CharField()

    def send_email(self):
        message = f"Ad: {self.cleaned_data.get('name')}\nEmail: {self.cleaned_data.get('email')}" \
                  f"\n\n{self.cleaned_data.get('message')}"
        try:
            mail = EmailMessage(
                subject=self.cleaned_data.get('topic'),
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[settings.EMAIL_HOST_USER],
                reply_to=[settings.EMAIL_HOST_USER],
            )
            mail.content_subtype = "html"
            return mail.send()
        except:
            return False


class EmailSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ('email',)

    def send_email(self, instance):
        message = render_to_string('email/new_subscription.html', {'email': self.cleaned_data.get('email'),
                                                                   'deactivate_url': instance.get_deactivate_url})
        try:
            mail = EmailMessage(
                subject="Petinven - E-bülten Aboneliğiniz Hakkında",
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[self.cleaned_data.get('email')],
                reply_to=[settings.EMAIL_HOST_USER]
            )
            mail.content_subtype = "html"
            mail.send()
            return True
        except:
            return False
