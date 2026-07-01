from django.urls import path
from django.views.generic import RedirectView
from .views import shorten_url, redirect_url

urlpatterns = [
    path('', RedirectView.as_view(url='/shorten/', permanent=False), name='home'),
    path("shorten/", shorten_url),
    path("<str:short_code>/", redirect_url),
]
