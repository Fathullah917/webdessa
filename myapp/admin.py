from django.contrib import admin
from .models import (
    Pengaduan, UMKM, APBDesa, DetailAPBDesa, Article, PotensiDesa,
    IdentitasUmum, DataKependudukan, PemerintahanDesa,
    JabatanPejabat, PejabatDesa, SaranaPrasarana, CarouselImage,
    PotensiGalleryImage # Pastikan ini diimpor
)

# Inline untuk Gambar Galeri Potensi
class PotensiGalleryImageInline(admin.TabularInline): # Atau admin.StackedInline jika ingin tampilan yang lebih vertikal
    model = PotensiGalleryImage
    extra = 1 # Menampilkan 1 form kosong tambahan untuk upload gambar baru
    fields = ('image', 'caption', 'order') # Bidang yang akan ditampilkan


# Admin kustom untuk PotensiDesa
@admin.register(PotensiDesa)
class PotensiDesaAdmin(admin.ModelAdmin):
    list_display = ('nama_potensi', 'jenis_potensi', 'lokasi', 'tanggal_publikasi')
    list_filter = ('jenis_potensi',)
    search_fields = ('nama_potensi', 'deskripsi', 'lokasi')
    inlines = [PotensiGalleryImageInline] # Menambahkan inline di sini

    fieldsets = (
        (None, {
            'fields': ('jenis_potensi', 'nama_potensi', 'deskripsi', 'gambar_utama', 'lokasi', 'link_detail', 'embed_video_link', 'peta_embed_code')
        }),
        ('Detail Informasi Wisata', {
            'fields': ('jam_operasional', 'harga_tiket', 'fasilitas', 'kegiatan_atraksi',
                       'pengelola_kontak', 'akomodasi_kuliner_sekitar', 'tips_peringatan'),
            'classes': ('collapse',), # Membuat bagian ini bisa dilipat
            'description': 'Isi hanya jika Jenis Potensi adalah "Wisata".'
        }),
        ('Detail Informasi Sumber Daya Alam (SDA)', {
            'fields': ('jenis_sda', 'luas_lokasi_sda', 'pemanfaatan_sda', 'nilai_ekonomi_sda',
                       'pengelola_sda', 'kendala_pengembangan_sda', 'link_pendukung_sda'),
            'classes': ('collapse',),
            'description': 'Isi hanya jika Jenis Potensi adalah "Sumber Daya Alam".'
        }),
        ('Detail Informasi UMKM', {
            'fields': ('nama_produk_umkm', 'jenis_usaha_umkm', 'deskripsi_produk_umkm',
                       'bahan_baku_umkm', 'skala_produksi_umkm', 'legalitas_umkm',
                       'pemasaran_umkm', 'alamat_umkm_detail', 'kontak_umkm_detail'),
            'classes': ('collapse',),
            'description': 'Isi hanya jika Jenis Potensi adalah "UMKM".'
        }),
        ('Detail Informasi Budaya & Kesenian Tradisional', {
            'fields': ('nama_budaya_kesenian', 'jenis_budaya_kesenian', 'deskripsi_makna_budaya',
                       'waktu_tempat_pelaksanaan', 'pelaku_penampil', 'nilai_historis_filosofis',
                       'upaya_pelestarian', 'potensi_wisata_budaya', 'kontak_narahubung_budaya'),
            'classes': ('collapse',),
            'description': 'Isi hanya jika Jenis Potensi adalah "Budaya & Kesenian Tradisional".'
        }),
    )


# Mendaftarkan model lain seperti biasa
admin.site.register(Pengaduan)
admin.site.register(UMKM) # Ini adalah model UMKM terpisah yang sudah ada
admin.site.register(APBDesa)
admin.site.register(DetailAPBDesa)
admin.site.register(Article)
# admin.site.register(PotensiDesa) # Hapus baris ini karena sudah didaftarkan dengan @admin.register
admin.site.register(IdentitasUmum)
admin.site.register(DataKependudukan)
admin.site.register(PemerintahanDesa)
admin.site.register(JabatanPejabat)
admin.site.register(PejabatDesa)
admin.site.register(SaranaPrasarana)
admin.site.register(CarouselImage)
# admin.site.register(PotensiGalleryImage) # Tidak perlu didaftarkan langsung jika sudah inline
