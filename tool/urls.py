from . import views
from django.urls import path


urlpatterns = [
    path('', views.signin,name='signin'),
    path('dashboard', views.dashboard,name='dashboard'),
    path('manage_slave', views.manage_slave,name='manage_slave'),
    path('manage_master', views.manage_master,name='manage_master'),
    path('groups_copier', views.groups_copier,name='groups_copier'),
    path('servers', views.servers,name='servers'),
    ]
