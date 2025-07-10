# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='index'), # Sudah benar
    
    # PERBAIKAN DI SINI: Ganti views.artikel_detail menjadi views.artikel_detail_view
    path('artikel/<int:pk>/', views.artikel_detail_view, name='artikel_detail'), 
    
    path('pengaduan/', views.pengaduan_view, name='pengaduan_view'),
    path('umkm/', views.umkm_view, name='umkm_view'),
    path('data-apbdesa/', views.dataAPBDes_view, name='dataAPBDes_view'),
    path('about/', views.about_view, name='about_view'),
]