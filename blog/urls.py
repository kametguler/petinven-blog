from django.urls import path
from .views import HomePage, PostDetailView, ContactUsView, EmailSubscriptionView, EmailSubscriptionDeactivateView

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('iletisim/', ContactUsView.as_view(), name='contact-us'),
    path('newsletter-activation/', EmailSubscriptionView.as_view(), name='subscription'),
    path('newsletter-deactivation/<slug>/', EmailSubscriptionDeactivateView.as_view(),
         name='subscription-deactivate'),
]
