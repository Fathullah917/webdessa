from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('berita/', views.article_list_view, name='article_list'),
    path('artikel/<int:pk>/', views.article_detail_view, name='article_detail'),
    path('pengaduan/', views.pengaduan_view, name='pengaduan'),
    path('pengaduan/daftar-publik/', views.daftar_pengaduan_publik_view, name='daftar_pengaduan_publik'),
    path('data-apbdes/', views.apbdesa_view, name='data_apbdesa'),
    path('data-apbdes/<int:tahun>/', views.detail_apbdesa_view, name='detail_apbdesa'),
    path('tentang/', views.about_view, name='about'),
    # URL untuk daftar semua potensi desa (jika ada halaman indeks umum)
    path('potensi-desa/', views.potensi_desa_index_view, name='potensi_desa_index'),

    # URL untuk daftar masing-masing jenis potensi
    path('potensi-desa/wisata/', views.wisata_view, name='wisata'),
    path('potensi-desa/sda/', views.sda_view, name='sda_list'),
    path('potensi-desa/budaya/', views.budaya_view, name='budaya_list'),
    path('potensi-desa/umkm/', views.umkm_list_view, name='umkm_list'),

    # URL tunggal untuk detail semua jenis potensi
    # Fungsi view 'potensi_detail_view' yang akan menentukan template mana yang akan dirender
    path('potensi-desa/<int:pk>/', views.potensi_detail_view, name='potensi_detail'),
    # Baris di bawah ini dihapus karena sudah ditangani oleh potensi_detail_view di atas
    # path('potensi-desa/wisata/<int:pk>/', views.wisata_detail, name='wisata_detail'),

    # URL profil desa
    path('profil/visi-misi-sejarah/', views.profil_visi_misi_sejarah_view, name='profil_visi_misi_sejarah'),
    path('profil/struktur-pemerintahan/', views.profil_struktur_view, name='profil_struktur'),
    path('profil/data-kependudukan-wilayah/', views.profil_kependudukan_wilayah_view, name='profil_kependudukan_wilayah'),
    path('profil/sarana-prasarana/', views.profil_sarana_prasarana_view, name='profil_sarana_prasarana'),
]
