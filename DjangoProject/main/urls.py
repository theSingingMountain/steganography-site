from django.conf import settings
from django.urls import path

from main.forms import UserLoginForm
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('home', views.homepage, name = "homepage"),
    path('registration', views.register, name = 'registration'),
    path('login',auth_views.LoginView.as_view(template_name = "login.html", authentication_form = UserLoginForm), name = "Login"),
    path('login/',auth_views.LoginView.as_view(template_name = "login.html", authentication_form = UserLoginForm), name = "Login"),
    path('logout',auth_views.LogoutView.as_view(template_name = 'home.html'), name = "Logout"),
    path('gallery', views.gallery, name = "Image Gallery"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)