from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/slots/', include('slots_app.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]
