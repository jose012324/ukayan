from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('view_staff/', views.view_staff, name='view_staff'),
    path('add_supply/', views.add_supply, name='add_supply'),
    path('outgoing_stock', views.outgoing_stock, name='outgoing_stock'),
    path('view_stock', views.view_stock, name='view_stock'),
    path('view_oldstock/', views.view_oldstock, name='view_oldstock'),
    path('view_report/', views.view_report, name='view_report'),
    path('staff_dashboard/',views.staff_dashboard, name='staff_dashboard'),
    path('report/', views.report, name='report'),
    path('view_table/', views.view_table, name='view_table'),
    path('loading/', views.loading, name='loading'),
    path('loading_view/', views.loading_view, name='loading_view'),
    path('logout/',views.logout_view, name='logout'),
]
