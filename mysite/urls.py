# mysite/mysite/urls.py from DJ4E

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

# Redirects different URL starters to respective files
urlpatterns = [
    path("polls/", include("polls.urls")),
    path("solo1/", include("solo1.urls")),
    path("hello/", include("hello.urls")),
    path("autos/", include("autos.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", TemplateView.as_view(template_name="home/main.html")),
    path("admin/", admin.site.urls),
]