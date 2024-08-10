from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add_phone, name="add_phone"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_view, name='search_view'),
    path('api/search/', views.phone_search_api, name='phone_search_api'),
    path('api/export/json/', views.json_export_view, name='json_export_view'),
    path("success/", views.success_view, name="success_add_phone"),
]