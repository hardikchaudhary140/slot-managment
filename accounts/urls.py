from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='api-login'),
    path('logout/', views.logout_view, name='api-logout'),
    path('me/', views.me, name='api-me'),
    path('', views.user_list_create, name='api-users'),
]
