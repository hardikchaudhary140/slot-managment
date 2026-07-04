from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie
from slots_app.views import BlockedDateViewSet

index_view = ensure_csrf_cookie(TemplateView.as_view(template_name='index.html'))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/slots/blocked-dates/check/', BlockedDateViewSet.as_view({'get': 'check'}), name='blocked-date-check'),
    path('api/slots/blocked-dates/<int:pk>/unblock/', BlockedDateViewSet.as_view({'post': 'unblock'}), name='blocked-date-unblock'),
    path('api/slots/blocked-dates/<int:pk>/', BlockedDateViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='blocked-date-detail'),
    path('api/slots/blocked-dates/', BlockedDateViewSet.as_view({'get': 'list', 'post': 'create'}), name='blocked-date-list'),
    path('api/slots/', include('slots_app.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('', index_view, name='index'),
]
