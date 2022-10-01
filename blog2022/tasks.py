from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from blog.models import NewsletterSubscription, Post
from blog2022 import settings


def weekly_email():
    subsc = NewsletterSubscription.objects.filter(is_active=True)
    popular_posts = sorted(Post.objects.filter(status=1)[:3], key=lambda a: a.get_hit_count, reverse=True)
    message = render_to_string('email/weekly_subscription.html', {'posts': popular_posts})
    try:
        mail = EmailMessage(
            subject="Petinven - E-bülten Aboneliğiniz Hakkında",
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[email.email for email in subsc],
            reply_to=[settings.EMAIL_HOST_USER]
        )
        mail.content_subtype = "html"
        mail.send()
        return True
    except:
        return 'Email gönderimi sırasında hata'
