from django.conf import settings
from django.http import HttpResponse
from django.urls import include, path


def home(request):
    """Serve the single-page website (index.html next to manage.py)."""
    html = (settings.BASE_DIR / "index.html").read_text(encoding="utf-8")
    return HttpResponse(html)


urlpatterns = [
    path("", home),
    path("api/", include("practice.urls")),
]
