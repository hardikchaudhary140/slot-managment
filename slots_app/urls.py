from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.SlotViewSet)

urlpatterns = [
    path('teams/', views.team_list, name='api-teams'),
    path('', include(router.urls)),
]
