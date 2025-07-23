from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('berita/', views.article_list_view, name='article_list'), # <-- Pastikan baris ini ada!
    path('artikel/<int:pk>/', views.article_detail_view, name='article_detail'),
    path('pengaduan/', views.pengaduan_view, name='pengaduan'),
    path('pengaduan/daftar-publik/', views.daftar_pengaduan_publik_view, name='daftar_pengaduan_publik'),
    path('data-apbdes/', views.apbdesa_view, name='data_apbdesa'),
    path('data-apbdes/<int:tahun>/', views.detail_apbdesa_view, name='detail_apbdesa'),
    path('tentang/', views.about_view, name='about'),
    path('potensi-desa/', views.potensi_desa_index_view, name='potensi_desa_index'),
    path('potensi-desa/wisata/', views.wisata_view, name='wisata'),
    path('potensi-desa/pertanian/', views.pertanian_view, name='pertanian'),
    path('potensi-desa/budaya/', views.budaya_view, name='budaya'),
    path('potensi-desa/umkm/', views.umkm_potensi_view, name='potensi_umkm'),
    path('potensi-desa/detail/<int:pk>/', views.potensi_desa_detail_view, name='potensi_desa_detail'),
]