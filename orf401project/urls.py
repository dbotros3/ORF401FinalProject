# orf401project/urls.py

from django.contrib import admin
from django.urls import include, path
from workout.views import home  # Ensure this is the correct import statement
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # This will set 'home' as the homepage view
    path('workout/', include('workout.urls')),    # ... include other app URLs if needed ...
    path('nutrition/', include('nutrition.urls')),
    path('accounts/', include('accounts.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
