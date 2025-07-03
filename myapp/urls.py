from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('pengaduan/', views.pengaduan_view, name='pengaduan_view'),
    path('umkm/', views.umkm_view, name='umkm_view'),
    path('data-apbdesa/', views.dataAPBDes_view, name='dataAPBDes_view'),
    path('about/', views.about_view, name='about_view'),
]