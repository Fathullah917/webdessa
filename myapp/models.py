from django.db import models
from django.core.exceptions import ValidationError

# Mixin untuk Model Singleton
class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError(f"Hanya boleh ada satu instance dari {self.__class__.__name__}.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Opsional: Cegah penghapusan jika hanya ada satu instance
        # if self.__class__.objects.count() == 1:
        #     raise ValidationError(f"Tidak bisa menghapus satu-satunya instance dari {self.__class__.__name__}.")
        super().delete(*args, **kwargs)


class IdentitasUmum(SingletonModel):
    nama_desa = models.CharField(max_length=100, default="Boyemare")
    nama_kecamatan = models.CharField(max_length=100, default="Sakra Barat")
    nama_kabupaten = models.CharField(max_length=100, default="Lombok Timur")
    nama_provinsi = models.CharField(max_length=100, default="Nusa Tenggara Barat")
    nama_kepala_desa = models.CharField(max_length=100, default="Ahmad Fathullah")
    sejarah_desa = models.TextField(
        help_text="Sejarah panjang desa, termasuk sebagai komunitas agraris, dll."
    )
    alamat_kantor = models.CharField(
        max_length=255, default="Jalan Raya Boyemare No. 123, Kec. Sakra Barat"
    )
    email_resmi = models.EmailField(
        max_length=255, blank=True, null=True, default="desaboyemare@example.com"
    )
    telepon_resmi = models.CharField(
        max_length=50, blank=True, null=True, default="+62 812-3456-7890"
    )
    visi_desa = models.TextField(
        blank=True, null=True, help_text="Visi Desa Boyemare"
    )
    misi_desa = models.TextField(
        blank=True, null=True, help_text="Misi Desa Boyemare (gunakan baris baru untuk setiap poin)"
    )

    class Meta:
        verbose_name_plural = "1. Identitas Umum Desa"

    def __str__(self):
        return f"Identitas Umum Desa {self.nama_desa}"


class DataKependudukan(SingletonModel):
    total_penduduk = models.IntegerField(default=0)
    jumlah_laki_laki = models.IntegerField(default=0)
    jumlah_perempuan = models.IntegerField(default=0)
    jumlah_kk = models.IntegerField(default=0)
    mayoritas_pekerjaan = models.CharField(
        max_length=255, default="petani, buruh, dan pelaku UMKM"
    )
    tingkat_pendidikan_umum = models.CharField(
        max_length=255, default="bervariasi dari SD hingga perguruan tinggi"
    )
    keberagaman_budaya = models.CharField(
        max_length=255, default="agama dan suku yang hidup rukun"
    )
    luas_wilayah = models.CharField(
        max_length=100, blank=True, null=True, help_text="Contoh: 12.34 km persegi"
    )
    batas_wilayah = models.TextField(
        blank=True, null=True, help_text="Contoh: Utara: Desa A, Selatan: Desa B, dst."
    )
    jumlah_dusun = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        verbose_name_plural = "2. Data Kependudukan & Wilayah"

    def __str__(self):
        return f"Data Kependudukan ({self.total_penduduk} jiwa)"


class PemerintahanDesa(SingletonModel):
    deskripsi_umum = models.TextField(
        help_text="Deskripsi umum tentang pemerintahan desa (Kepala Desa, perangkat, BPD)"
    )
    lembaga_pendukung = models.TextField(
        help_text="Dukungan lembaga seperti PKK, Karang Taruna, LPMD (pisahkan dengan koma atau enter)"
    )
    proses_perencanaan = models.TextField(
        help_text="Proses perencanaan pembangunan (RPJMDes, RKPDes)"
    )

    class Meta:
        verbose_name_plural = "3. Pemerintahan Desa (Umum)"

    def __str__(self):
        return "Informasi Umum Pemerintahan Desa"


class JabatanPejabat(models.Model):
    nama_jabatan = models.CharField(max_length=100, unique=True)
    urutan = models.IntegerField(default=99, help_text="Untuk mengatur urutan tampilan jabatan")

    class Meta:
        verbose_name = "Jabatan Pejabat"
        verbose_name_plural = "Jabatan Pejabat"
        ordering = ['urutan', 'nama_jabatan']

    def __str__(self):
        return self.nama_jabatan

class PejabatDesa(models.Model):
    nama_lengkap = models.CharField(max_length=200)
    jabatan = models.ForeignKey(JabatanPejabat, on_delete=models.SET_NULL, null=True, blank=True,
                                 help_text="Pilih jabatan dari daftar yang tersedia")
    foto = models.ImageField(upload_to='pejabat_desa/', blank=True, null=True)
    periode_jabatan = models.CharField(max_length=100, blank=True, null=True,
                                       help_text="Contoh: 2020-2025")
    kontak_info = models.CharField(max_length=255, blank=True, null=True,
                                   help_text="Kontak atau informasi lain (opsional)")
    urutan_tampil = models.IntegerField(default=99, help_text="Untuk mengatur urutan tampilan pejabat")

    class Meta:
        verbose_name = "Pejabat Desa"
        verbose_name_plural = "3a. Daftar Pejabat Desa" # Sub-menu di admin
        ordering = ['urutan_tampil', 'nama_lengkap']

    def __str__(self):
        return f"{self.nama_lengkap} ({self.jabatan if self.jabatan else 'Tidak Ada Jabatan'})"


class SaranaPrasarana(SingletonModel):
    akses_jalan_utama = models.TextField(help_text="Deskripsi akses jalan utama")
    fasilitas_pendidikan = models.TextField(help_text="Contoh: PAUD, TK, SD, SMP, SMA")
    layanan_kesehatan = models.TextField(help_text="Contoh: Puskesmas Pembantu, Posyandu, Bidan Desa")
    tempat_ibadah = models.TextField(help_text="Contoh: Masjid, Gereja, Pura (pisahkan dengan koma)")
    jaringan_listrik_air = models.TextField(help_text="Deskripsi cakupan jaringan listrik dan air bersih")
    fasilitas_umum_lain = models.TextField(
        blank=True, null=True, help_text="Contoh: pasar, balai desa, jaringan internet, dll."
    )

    class Meta:
        verbose_name_plural = "4. Sarana dan Prasarana Umum"

    def __str__(self):
        return "Informasi Sarana dan Prasarana"

# --- Model untuk Artikel/Berita ---
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    gambar_utama = models.ImageField(
        upload_to='article_images/', # Gambar akan disimpan di media/article_images/
        blank=True,
        null=True,
        help_text="Unggah gambar utama untuk artikel ini."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Artikel & Berita"
        ordering = ['-created_at'] # Urutkan dari yang terbaru

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
    nomor_telepon = models.CharField(max_length=20, blank=True, null=1)

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
        upload_to='pengaduan_bukti/', # Gambar akan disimpan di media/pengaduan_bukti/
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

# --- Model untuk UMKM (ini adalah model terpisah, bukan bagian dari PotensiDesa) ---
class UMKM(models.Model):
    nama_umkm = models.CharField(max_length=150)
    jenis_usaha = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)
    nama_pemilik = models.CharField(max_length=100)
    kontak_pemilik = models.CharField(max_length=50, blank=True, null=True) # Kontak umum, bisa WA/Telp
    alamat = models.TextField(blank=True, null=True)
    tahun_berdiri = models.IntegerField(blank=True, null=True)
    logo_umkm = models.ImageField(upload_to='umkm_logos/', blank=True, null=True) # Logo UMKM (kecil)
    gambar_produk = models.ImageField( # Gambar yang lebih representatif untuk display
        upload_to='umkm_produk_images/', # Gambar akan disimpan di media/umkm_produk_images/
        blank=True,
        null=True,
        help_text="Unggah gambar produk utama atau tampilan UMKM ini."
    )
    no_telepon = models.CharField(max_length=20, blank=True, null=True, verbose_name="Nomor Telepon/WA")
    link_medsos = models.URLField(max_length=200, blank=True, null=True, verbose_name="Link Media Sosial/Website")


    class Meta:
        verbose_name_plural = "Daftar UMKM"
        ordering = ['nama_umkm'] # Urutkan berdasarkan nama UMKM

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
        ordering = ['-tahun'] # Urutkan dari tahun terbaru

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

# --- MODEL UTAMA UNTUK POTENSI DESA (Wisata, Pertanian, Budaya, dll.) ---
class PotensiDesa(models.Model):
    JENIS_POTENSI_CHOICES = [
        ('Wisata', 'Wisata'),
        ('SDA', 'Sumber Daya Alam'),
        ('UMKM', 'Usaha Mikro, Kecil, dan Menengah'),
        ('Budaya', 'Budaya & Kesenian Tradisional'),
        ('Lain-lain', 'Lain-lain'),
    ]

    jenis_potensi = models.CharField(
        max_length=50,
        choices=JENIS_POTENSI_CHOICES,
        help_text="Pilih jenis potensi desa ini (misal: Wisata, Sumber Daya Alam)."
    )
    nama_potensi = models.CharField(max_length=200, verbose_name="Nama Potensi / Judul")
    deskripsi = models.TextField(help_text="Deskripsi singkat atau daya tarik utama potensi ini.")

    # --- Bidang Umum untuk semua jenis potensi (jika relevan) ---
    gambar_utama = models.ImageField(
        upload_to='potensi_desa_images/', # Gambar akan disimpan di media/potensi_desa_images/
        blank=True,
        null=True,
        help_text="Unggah gambar utama yang merepresentasikan potensi ini."
    )
    lokasi = models.CharField(max_length=255, blank=True, null=True, help_text="Lokasi spesifik potensi ini (contoh: Dukuh A, Jalur Sungai).")
    link_detail = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Link eksternal (misal: Google Maps, artikel terkait) atau biarkan kosong jika tidak ada."
    )
    tanggal_publikasi = models.DateTimeField(auto_now_add=True)
    embed_video_link = models.URLField(max_length=500, blank=True, null=True,
                                       help_text="Link video YouTube/Vimeo (opsional).")
    peta_embed_code = models.TextField( # Bidang untuk kode embed peta spesifik per potensi
        blank=True,
        null=True,
        help_text="Kode embed Google Maps untuk lokasi potensi ini (misal: dari 'Sematkan peta' di Google Maps)."
    )

    # --- Bidang Khusus untuk 'Wisata' ---
    jam_operasional = models.CharField(max_length=255, blank=True, null=True,
                                       help_text="Contoh: Setiap hari, 08.00 - 17.00 WITA (Khusus Wisata)")
    harga_tiket = models.CharField(max_length=255, blank=True, null=True,
                                   help_text="Contoh: Gratis, Rp 10.000/orang, Bervariasi (Khusus Wisata)")
    fasilitas = models.TextField(blank=True, null=True,
                                 help_text="Daftar fasilitas yang tersedia di lokasi wisata. Pisahkan dengan baris baru. (Khusus Wisata)")
    kegiatan_atraksi = models.TextField(blank=True, null=True,
                                        help_text="Daftar kegiatan atau atraksi unggulan yang bisa dilakukan. Pisahkan dengan baris baru. (Khusus Wisata)")
    pengelola_kontak = models.TextField(blank=True, null=True,
                                        help_text="Nama pengelola dan informasi kontak (telepon/email). (Khusus Wisata)")
    akomodasi_kuliner_sekitar = models.TextField(blank=True, null=True,
                                                 help_text="Informasi penginapan dan tempat makan di sekitar lokasi. Pisahkan dengan baris baru. (Khusus Wisata)")
    tips_peringatan = models.TextField(blank=True, null=True,
                                       help_text="Tips untuk pengunjung dan peringatan penting. Pisahkan dengan baris baru. (Khusus Wisata)")


    # --- Bidang Khusus untuk 'SDA' (Sumber Daya Alam) ---
    jenis_sda = models.CharField(max_length=100, blank=True, null=True,
                                 help_text="Jenis SDA: Hayati / Non-hayati (air, tanah, mineral, hasil hutan, hasil laut, dll). (Khusus SDA)")
    luas_lokasi_sda = models.TextField(blank=True, null=True,
                                       help_text="Luas lahan, letak geografis, akses menuju lokasi SDA. (Khusus SDA)")
    pemanfaatan_sda = models.TextField(blank=True, null=True,
                                       help_text="Bagaimana potensi SDA digunakan saat ini? Oleh siapa? (Khusus SDA)")
    nilai_ekonomi_sda = models.TextField(blank=True, null=True,
                                         help_text="Dampak terhadap ekonomi desa dari SDA. (Khusus SDA)")
    pengelola_sda = models.CharField(max_length=255, blank=True, null=True,
                                     help_text="Dikelola oleh BUMDes, Kelompok Tani Hutan, dll. (Khusus SDA)")
    kendala_pengembangan_sda = models.TextField(blank=True, null=True,
                                                help_text="Kendala dan potensi pengembangan SDA. Pisahkan dengan baris baru. (Khusus SDA)")
    link_pendukung_sda = models.URLField(max_length=500, blank=True, null=True,
                                         help_text="Link pendukung terkait SDA (jika ada). (Khusus SDA)")

    # --- Bidang Khusus untuk 'UMKM' ---
    nama_produk_umkm = models.CharField(max_length=200, blank=True, null=True,
                                        help_text="Nama UMKM / Produk Unggulan. (Khusus UMKM)")
    jenis_usaha_umkm = models.CharField(max_length=100, blank=True, null=True,
                                        help_text="Jenis Usaha: Makanan, kerajinan, pakaian, pertanian olahan, dll. (Khusus UMKM)")
    deskripsi_produk_umkm = models.TextField(blank=True, null=True,
                                             help_text="Deskripsi singkat produk / jasa UMKM. (Khusus UMKM)")
    bahan_baku_umkm = models.CharField(max_length=255, blank=True, null=True,
                                       help_text="Bahan baku: Lokal atau dari luar? (Khusus UMKM)")
    skala_produksi_umkm = models.CharField(max_length=255, blank=True, null=True,
                                           help_text="Skala produksi & jumlah pekerja. (Khusus UMKM)")
    legalitas_umkm = models.CharField(max_length=255, blank=True, null=True,
                                      help_text="Legalitas Usaha: (NIB, PIRT, Halal, BPOM, dll). Pisahkan dengan koma. (Khusus UMKM)")
    pemasaran_umkm = models.CharField(max_length=255, blank=True, null=True,
                                      help_text="Pemasaran: Offline (pasar lokal) / Online (Shopee, WA, Instagram). (Khusus UMKM)")
    alamat_umkm_detail = models.TextField(blank=True, null=True,
                                          help_text="Alamat lokasi usaha UMKM. (Khusus UMKM)")
    kontak_umkm_detail = models.TextField(blank=True, null=True,
                                          help_text="Nomor HP, WA, Sosmed UMKM. Pisahkan dengan baris baru. (Khusus UMKM)")

    # --- Bidang Khusus untuk 'Budaya' ---
    nama_budaya_kesenian = models.CharField(max_length=200, blank=True, null=True,
                                            help_text="Nama Budaya/Kesenian (misal: Gendang Beleq, Peresean, Tari Gandrung). (Khusus Budaya)")
    jenis_budaya_kesenian = models.CharField(max_length=100, blank=True, null=True,
                                             help_text="Jenis: Seni pertunjukan, tradisi adat, tarian, musik, pakaian, kuliner khas, dll. (Khusus Budaya)")
    deskripsi_makna_budaya = models.TextField(blank=True, null=True,
                                              help_text="Deskripsi & makna budaya. (Khusus Budaya)")
    waktu_tempat_pelaksanaan = models.TextField(blank=True, null=True,
                                                help_text="Waktu & Tempat Pelaksanaan (jika event/tahunan). Pisahkan dengan baris baru. (Khusus Budaya)")
    pelaku_penampil = models.TextField(blank=True, null=True,
                                       help_text="Pelaku/Penampil: Kelompok seni, tokoh adat. Pisahkan dengan baris baru. (Khusus Budaya)")
    nilai_historis_filosofis = models.TextField(blank=True, null=True,
                                                help_text="Nilai Historis atau Filosofis budaya. (Khusus Budaya)")
    upaya_pelestarian = models.TextField(blank=True, null=True,
                                         help_text="Upaya Pelestarian: Dukungan desa, sekolah, komunitas. Pisahkan dengan baris baru. (Khusus Budaya)")
    potensi_wisata_budaya = models.TextField(blank=True, null=True,
                                             help_text="Potensi Wisata Budaya. (Khusus Budaya)")
    kontak_narahubung_budaya = models.CharField(max_length=255, blank=True, null=True,
                                                help_text="Kontak Narahubung (bila ingin tampil di event). (Khusus Budaya)")


    class Meta:
        verbose_name_plural = "Potensi Desa"
        ordering = ['jenis_potensi', 'nama_potensi'] # Urutkan berdasarkan jenis lalu nama

    def __str__(self):
        return f"{self.jenis_potensi}: {self.nama_potensi}"

# --- MODEL BARU UNTUK GALERI FOTO POTENSI DESA ---
class PotensiGalleryImage(models.Model):
    potensi = models.ForeignKey(PotensiDesa, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='potensi_gallery/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Urutan tampilan gambar dalam galeri")

    class Meta:
        ordering = ['order']
        verbose_name = "Gambar Galeri Potensi"
        verbose_name_plural = "Gambar Galeri Potensi"

    def __str__(self):
        return f"Gambar Galeri untuk {self.potensi.nama_potensi} ({self.order})"


# --- MODEL UNTUK GAMBAR CAROUSEL HERO (DIUBAH DARI WISATACAROUSELIMAGE) ---
class CarouselImage(models.Model):
    # Menggunakan pilihan yang sama dengan PotensiDesa untuk konsistensi
    JENIS_POTENSI_CHOICES = [
        ('Wisata', 'Wisata'),
        ('SDA', 'Sumber Daya Alam'),
        ('UMKM', 'Usaha Mikro, Kecil, dan Menengah'),
        ('Budaya', 'Budaya & Kesenian Tradisional'),
        ('Umum', 'Umum (untuk halaman lain jika diperlukan)'), # Tambahkan 'Umum' jika ada carousel di halaman non-potensi
    ]
    
    image = models.ImageField(upload_to='carousel_images/') # Folder tempat gambar akan disimpan
    caption = models.CharField(max_length=255, blank=True, null=True)
    jenis_potensi = models.CharField(
        max_length=50,
        choices=JENIS_POTENSI_CHOICES,
        default='Umum', # Default ke 'Umum' jika tidak spesifik
        help_text="Pilih jenis potensi yang akan menggunakan gambar ini di carousel hero."
    )
    order = models.IntegerField(default=0, help_text="Urutan tampilan gambar (lebih kecil muncul lebih dulu)")

    class Meta:
        ordering = ['jenis_potensi', 'order'] # Mengurutkan gambar berdasarkan jenis lalu order
        verbose_name = "Gambar Carousel Hero"
        verbose_name_plural = "Gambar Carousel Hero"

    def __str__(self):
        return f"{self.jenis_potensi} Carousel: {self.caption if self.caption else f'Gambar {self.id}'}"
