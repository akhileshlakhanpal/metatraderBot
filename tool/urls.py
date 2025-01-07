

from django.urls import path
from django_distill import distill_path
from . import views

def get_signin_url():
    return None

def get_dashboard_url():
    return None

def get_manage_slave_url():
    return None

def get_manage_master_url():
    return None

def get_groups_copier_url():
    return None

def get_servers_url():
    return None

urlpatterns = [
    distill_path('', views.signin, name='signin', distill_func=get_signin_url),
    distill_path('dashboard', views.dashboard, name='dashboard', distill_func=get_dashboard_url),
    distill_path('manage_slave', views.manage_slave, name='manage_slave', distill_func=get_manage_slave_url),
    distill_path('manage_master', views.manage_master, name='manage_master', distill_func=get_manage_master_url),
    distill_path('groups_copier', views.groups_copier, name='groups_copier', distill_func=get_groups_copier_url),
    distill_path('servers', views.servers, name='servers', distill_func=get_servers_url),
]
