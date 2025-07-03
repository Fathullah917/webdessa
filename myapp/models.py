from django.db import models

# --- Model untuk Artikel/Berita ---
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    gambar_utama = models.ImageField(
        upload_to='article_images/',
        blank=True,
        null=True,
        help_text="Unggah gambar utama untuk artikel ini."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Artikel & Berita"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

# --- Model untuk Pengaduan ---
class Pengaduan(models.Model):
    JENIS_PENGADUAN_CHOICES = [
        ('', '[ PILIH JENIS PENGADUAN ]'),
        ('Administrasi Kependudukan', 'Administrasi Kependudukan'),
        ('Jalan & Infrastruktur', 'Jalan & Infrastruktur'),
        ('Bantuan Sosial / BLT', 'Bantuan Sosial / BLT'),
        ('Lingkungan Hidup', 'Lingkungan Hidup'),
        ('Sengketa Tanah / Warga', 'Sengketa Tanah / Warga'),
        ('Pelayanan Pemerintah Desa', 'Pelayanan Pemerintah Desa'),
        ('Keamanan & Ketertiban', 'Keamanan & Ketertiban'),
    ]

    nama_pelapor = models.CharField(max_length=100)
    email_pelapor = models.EmailField(blank=True, null=True)
    nomor_telepon = models.CharField(max_length=20, blank=True, null=True)
    
    jenis_pengaduan = models.CharField(
        max_length=100,
        choices=JENIS_PENGADUAN_CHOICES,
        default='',
        help_text="Pilih jenis pengaduan Anda."
    )

    judul_pengaduan = models.CharField(max_length=200)
    isi_pengaduan = models.TextField()
    tanggal_pengaduan = models.DateTimeField(auto_now_add=True)
    
    bukti_foto = models.ImageField(
        upload_to='pengaduan_bukti/',
        blank=True,
        null=True,
        help_text="Unggah foto sebagai bukti jika ada."
    )

    status_pengaduan = models.CharField(
        max_length=50,
        choices=[
            ('Baru', 'Baru'),
            ('Dalam Proses', 'Dalam Proses'),
            ('Selesai', 'Selesai'),
            ('Ditolak', 'Ditolak')
        ],
        default='Baru'
    )

    class Meta:
        verbose_name_plural = "Pengaduan"

    def __str__(self):
        return f"Pengaduan dari {self.nama_pelapor} - {self.judul_pengaduan}"

# --- Model untuk UMKM ---
class UMKM(models.Model):
    nama_umkm = models.CharField(max_length=150)
    jenis_usaha = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)
    nama_pemilik = models.CharField(max_length=100)
    kontak_pemilik = models.CharField(max_length=50, blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    tahun_berdiri = models.IntegerField(blank=True, null=True)
    logo_umkm = models.ImageField(upload_to='umkm_logos/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Daftar UMKM"

    def __str__(self):
        return self.nama_umkm

# --- Model untuk APBDesa ---
class APBDesa(models.Model):
    tahun = models.IntegerField(unique=True)
    total_pendapatan = models.DecimalField(max_digits=15, decimal_places=2)
    total_belanja = models.DecimalField(max_digits=15, decimal_places=2)
    sisa_lebih_pembiayaan_anggaran = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    link_dokumen_resmi = models.URLField(max_length=500, blank=True, null=True)
    tanggal_publikasi = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Data APBDesa"
        ordering = ['-tahun']

    def __str__(self):
        return f"APBDesa Tahun {self.tahun}"

# --- Model opsional untuk detail item APBDesa (misal: belanja per kategori) ---
class DetailAPBDesa(models.Model):
    apbdesa = models.ForeignKey(APBDesa, on_delete=models.CASCADE, related_name='details')
    kategori = models.CharField(max_length=100)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    deskripsi_item = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Detail APBDesa"

    def __str__(self):
        return f"{self.kategori} ({self.apbdesa.tahun})"