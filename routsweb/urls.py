from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('routs/', include('routs.urls')), # добавление дочернего сопоставителя адресов
    path('', RedirectView.as_view(url='/routs/', permanent=True)), # перенаправление запроса домашней страницы на адрес /routs/
    path('healthz/', include('watchman.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
