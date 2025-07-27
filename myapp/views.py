from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages

# Impor form yang baru saja Anda definsikan
from .forms import PengaduanForm

# Impor semua model yang relevan dari aplikasi saat ini
from .models import (
    Pengaduan, UMKM, APBDesa, DetailAPBDesa, Article, PotensiDesa,
    IdentitasUmum, DataKependudukan, PemerintahanDesa,
    JabatanPejabat, PejabatDesa, SaranaPrasarana,
    CarouselImage, # Diimpor model CarouselImage yang baru
    PotensiGalleryImage
)

# Helper function untuk mengambil satu instance dari model Singleton
def get_single_instance(model):
    """
    Mengambil satu instance dari model. Jika ada lebih dari satu,
    mengambil yang pertama. Mengembalikan None jika tidak ada.
    """
    try:
        return model.objects.get()
    except model.DoesNotExist:
        return None
    except model.MultipleObjectsReturned:
        # Ini seharusnya tidak terjadi jika model diatur sebagai Singleton
        # di admin, tapi sebagai fallback, ambil yang pertama
        return model.objects.first()


# --- Home View ---
def home_view(request):
    articles = Article.objects.all().order_by('-created_at')

    selected_time_period = request.GET.get('time_period')

    if selected_time_period:
        now = timezone.now()
        if selected_time_period == 'today':
            articles = articles.filter(created_at__date=now.date())
        elif selected_time_period == 'this_week':
            start_of_week = now - timedelta(days=now.weekday()) # Monday as start of week
            articles = articles.filter(created_at__gte=start_of_week.date())
        elif selected_time_period == 'this_month':
            articles = articles.filter(created_at__year=now.year, created_at__month=now.month)
        elif selected_time_period == 'this_year':
            articles = articles.filter(created_at__year=now.year)
    
    # Batasi jumlah artikel untuk ditampilkan di beranda (misalnya untuk carousel)
    articles = articles[:12] 

    context = {
        'articles': articles,
        'selected_time_period': selected_time_period,
        'page_title': 'Beranda Desa Boyemare' # Tambahkan page_title untuk konsistensi
    }
    return render(request, 'home.html', context)


# --- Article Views ---
def article_list_view(request):
    filter_option = request.GET.get('filter', 'all')
    articles = Article.objects.all().order_by('-created_at')

    now = timezone.now().date() # Mengambil tanggal saat ini
    
    if filter_option == 'this_week':
        start_of_week = now - timedelta(days=now.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        articles = articles.filter(created_at__date__range=[start_of_week, end_of_week])
    elif filter_option == 'this_month':
        articles = articles.filter(created_at__year=now.year, created_at__month=now.month)
    elif filter_option == 'this_year':
        articles = articles.filter(created_at__year=now.year)
    # 'all' filter handled by default query

    context = {
        'all_articles': articles,
        'page_title': 'Semua Berita & Artikel',
        'active_filter': filter_option
    }
    return render(request, 'article_list.html', context)

def article_detail_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    context = {
        'article': article,
        'page_title': article.title
    }
    return render(request, 'artikel_detail.html', context)


# --- Pengaduan Views ---
def pengaduan_view(request):
    if request.method == 'POST':
        form = PengaduanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pengaduan Anda berhasil dikirim!')
            return redirect('pengaduan') # Redirect ke halaman yang sama setelah sukses
        else:
            messages.error(request, 'Terjadi kesalahan. Mohon periksa kembali isian formulir.')
    else:
        form = PengaduanForm() # Inisialisasi form untuk GET request

    # Logika untuk daftar pengaduan dan statistik
    # Mendapatkan 5 pengaduan terbaru (sesuaikan jika ingin lebih banyak)
    pengaduan_list = Pengaduan.objects.all().order_by('-tanggal_pengaduan')[:5] 
    
    # Menghitung statistik pengaduan mingguan
    now = timezone.now()
    # Menentukan awal minggu (misal: Senin)
    start_of_week = now - timedelta(days=now.weekday()) 
    semua_pengaduan_minggu_ini = Pengaduan.objects.filter(tanggal_pengaduan__gte=start_of_week)

    pengaduan_mingguan = semua_pengaduan_minggu_ini.count()

    # Pastikan nama field status_pengaduan di model Pengaduan Anda adalah 'status_pengaduan'
    # Dan nilai status ('Baru', 'Dalam Proses', 'Selesai', 'Ditolak') cocok dengan pilihan di model Anda
    pengaduan_status_mingguan = {
        'Baru': semua_pengaduan_minggu_ini.filter(status_pengaduan='Baru').count(),
        'Dalam_Proses': semua_pengaduan_minggu_ini.filter(status_pengaduan='Dalam Proses').count(),
        'Selesai': semua_pengaduan_minggu_ini.filter(status_pengaduan='Selesai').count(),
        'Ditolak': semua_pengaduan_minggu_ini.filter(status_pengaduan='Ditolak').count(),
    }

    context = {
        'form': form, # TERUSKAN OBJEK FORM INI KE TEMPLATE
        'page_title': 'Formulir Pengaduan',
        'pengaduan_list': pengaduan_list, # Untuk bagian "Daftar Judul Pengaduan Terbaru"
        'pengaduan_mingguan': pengaduan_mingguan, # Untuk statistik
        'pengaduan_status_mingguan': pengaduan_status_mingguan, # Untuk statistik
    }
    return render(request, 'pengaduan.html', context)

def daftar_pengaduan_publik_view(request):
    # Menampilkan pengaduan dengan status tertentu untuk publik
    public_pengaduans = Pengaduan.objects.filter(status_pengaduan__in=['Dalam Proses', 'Selesai']).order_by('-tanggal_pengaduan')
    context = {
        'public_pengaduans': public_pengaduans,
        'page_title': 'Daftar Pengaduan Publik'
    }
    return render(request, 'daftar_pengaduan_publik.html', context)


# --- APBDesa Views ---
def apbdesa_view(request):
    apbdesa_list = APBDesa.objects.all().order_by('-tahun') 
    context = {
        'apbdesa_list': apbdesa_list,
        'page_title': 'Data APBDesa'
    }
    return render(request, 'dataAPBDes.html', context)

def detail_apbdesa_view(request, tahun):
    apbdesa = get_object_or_404(APBDesa, tahun=tahun)
    detail_items = apbdesa.details.all() # Akses melalui related_name 'details'
    context = {
        'apbdesa': apbdesa,
        'detail_items': detail_items,
        'page_title': f'Detail APBDesa Tahun {tahun}'
    }
    return render(request, 'detail_apbdesa.html', context)


# --- Profil Desa Views ---

def profil_visi_misi_sejarah_view(request):
    identitas_umum = get_single_instance(IdentitasUmum)
    
    context = {
        'judul_halaman': 'Visi, Misi & Sejarah Desa Boyemare',
        'identitas_umum': identitas_umum,
    }
    if not identitas_umum:
        messages.warning(request, "Data Identitas Umum, Visi, Misi, atau Sejarah belum lengkap. Harap lengkapi di halaman admin.")
    return render(request, 'profil/visi_misi_sejarah.html', context)

def profil_struktur_view(request):
    pemerintahan_desa = get_single_instance(PemerintahanDesa)
    # Urutkan pejabat berdasarkan urutan tampil, lalu jabatan, lalu nama
    pejabat_desa = PejabatDesa.objects.select_related('jabatan').all().order_by('urutan_tampil', 'jabatan__urutan', 'nama_lengkap')
    
    context = {
        'judul_halaman': 'Struktur Pemerintahan Desa Boyemare',
        'pemerintahan_desa': pemerintahan_desa,
        'pejabat_desa': pejabat_desa,
    }
    if not pemerintahan_desa and not pejabat_desa.exists():
        messages.warning(request, "Data Struktur Pemerintahan atau Daftar Pejabat belum lengkap. Harap lengkapi di halaman admin.")
    return render(request, 'profil/struktur_pemerintahan.html', context)

def profil_kependudukan_wilayah_view(request):
    data_kependudukan = get_single_instance(DataKependudukan)
    # SaranaPrasarana juga bisa berisi info terkait wilayah (misal: luas, batas)
    sarana_prasarana = get_single_instance(SaranaPrasarana) 

    context = {
        'judul_halaman': 'Data Kependudukan & Wilayah Desa Boyemare',
        'data_kependudukan': data_kependudukan,
        'sarana_prasarana': sarana_prasarana, # Digunakan untuk peta dan info wilayah
    }
    if not data_kependudukan and not sarana_prasarana:
        messages.warning(request, "Data Kependudukan atau Wilayah belum lengkap. Harap lengkapi di halaman admin.")
    return render(request, 'profil/data_kependudukan_wilayah.html', context)

def profil_sarana_prasarana_view(request):
    sarana_prasarana = get_single_instance(SaranaPrasarana)

    context = {
        'judul_halaman': 'Sarana dan Prasarana Umum Desa Boyemare',
        'sarana_prasarana': sarana_prasarana,
    }
    if not sarana_prasarana:
        messages.warning(request, "Data Sarana dan Prasarana Umum belum lengkap. Harap lengkapi di halaman admin.")
    return render(request, 'profil/sarana_prasarana.html', context)

def profil_desa_lengkap_view(request):
    # View ini menggabungkan semua data profil desa
    identitas_umum = get_single_instance(IdentitasUmum)
    data_kependudukan = get_single_instance(DataKependudukan)
    pemerintahan_desa = get_single_instance(PemerintahanDesa)
    pejabat_desa = PejabatDesa.objects.select_related('jabatan').all().order_by('urutan_tampil', 'jabatan__urutan', 'nama_lengkap')
    sarana_prasarana = get_single_instance(SaranaPrasarana)

    context = {
        'judul_halaman': 'Profil Lengkap Desa Boyemare',
        'identitas_umum': identitas_umum,
        'data_kependudukan': data_kependudukan,
        'pemerintahan_desa': pemerintahan_desa,
        'pejabat_desa': pejabat_desa,
        'sarana_prasarana': sarana_prasarana,
    }
    # Anda bisa menambahkan pesan peringatan di sini juga jika ada data yang kosong
    return render(request, 'profil/profil_desa_lengkap.html', context)


# --- About Us View ---
def about_view(request):
    context = {
        'page_title': 'Tentang Kami',
        'description_text': 'Halaman ini berisi informasi mengenai visi, misi, dan sejarah Desa Boyemare.'
    }
    return render(request, 'about.html', context)


# --- Potensi Desa Views ---
def potensi_desa_index_view(request):
    all_potensi = PotensiDesa.objects.all().order_by('-tanggal_publikasi')

    for i, potensi in enumerate(all_potensi):
        potensi.animation_delay = (i + 1) * 0.1 

    context = {
        'potensi_list': all_potensi,
        'page_title': 'Semua Potensi Desa Buwun Mas',
        'description_text': 'Jelajahi berbagai potensi yang ada di Desa Buwun Mas, mulai dari wisata, pertanian, budaya, hingga UMKM lokal.'
    }
    return render(request, 'potensi_desa.html', context)

# View untuk daftar Wisata
def wisata_view(request):
    title_text = "Wisata Desa Buwun Mas"
    description_text = "Jelajahi keindahan alam dan daya tarik wisata yang memukau di Desa B."

    potensi_list = PotensiDesa.objects.filter(jenis_potensi='Wisata').order_by('nama_potensi')

    for i, potensi in enumerate(potensi_list):
        potensi.animation_delay = (i + 1) * 0.1

    # Mengambil gambar carousel khusus untuk Wisata
    carousel_images = CarouselImage.objects.filter(jenis_potensi='Wisata').order_by('order')

    context = {
        'title_text': title_text,
        'description_text': description_text,
        'potensi_list': potensi_list,
        'carousel_images': carousel_images,
    }
    return render(request, 'wisata.html', context)

# View untuk daftar Sumber Daya Alam
def sda_view(request):
    title_text = "Sumber Daya Alam Desa Buwun Mas"
    description_text = "Temukan kekayaan sumber daya alam yang melimpah di Desa Buwun Mas."

    potensi_list = PotensiDesa.objects.filter(jenis_potensi='SDA').order_by('nama_potensi')

    for i, potensi in enumerate(potensi_list):
        potensi.animation_delay = (i + 1) * 0.1

    # Mengambil gambar carousel khusus untuk SDA
    carousel_images = CarouselImage.objects.filter(jenis_potensi='SDA').order_by('order')

    context = {
        'title_text': title_text,
        'description_text': description_text,
        'potensi_list': potensi_list,
        'carousel_images': carousel_images,
    }
    return render(request, 'sda.html', context)

# View untuk daftar Budaya & Kesenian Tradisional
def budaya_view(request):
    title_text = "Budaya & Kesenian Tradisional Desa Boyemare"
    description_text = "Jelajahi kekayaan seni tradisional, adat istiadat, upacara, dan warisan budaya yang dijunjung tinggi di Desa Boyemare."

    potensi_list = PotensiDesa.objects.filter(jenis_potensi='Budaya').order_by('nama_potensi')

    for i, potensi in enumerate(potensi_list):
        potensi.animation_delay = (i + 1) * 0.1

    # Mengambil gambar carousel khusus untuk Budaya
    carousel_images = CarouselImage.objects.filter(jenis_potensi='Budaya').order_by('order')

    context = {
        'title_text': title_text,
        'description_text': description_text,
        'potensi_list': potensi_list,
        'carousel_images': carousel_images,
    }
    return render(request, 'budaya.html', context)

# View untuk daftar UMKM
def umkm_list_view(request):
    title_text = "Usaha Mikro, Kecil, dan Menengah (UMKM) Desa Boyemare"
    description_text = "Dukung produk lokal dan temukan beragam UMKM unggulan dari Desa Boyemare."

    potensi_list = PotensiDesa.objects.filter(jenis_potensi='UMKM').order_by('nama_potensi')

    for i, potensi in enumerate(potensi_list):
        potensi.animation_delay = (i + 1) * 0.1

    # Mengambil gambar carousel khusus untuk UMKM
    carousel_images = CarouselImage.objects.filter(jenis_potensi='UMKM').order_by('order')

    context = {
        'title_text': title_text,
        'description_text': description_text,
        'potensi_list': potensi_list,
        'carousel_images': carousel_images,
    }
    return render(request, 'umkm.html', context)


# View generik untuk detail potensi (akan merender template berbeda berdasarkan jenis potensi)
def potensi_detail_view(request, pk):
    potensi = get_object_or_404(PotensiDesa, pk=pk)
    gallery_images = potensi.gallery_images.all()

    # --- Pemrosesan bidang teks multi-baris (splitlines) ---
    # Untuk Wisata
    if potensi.fasilitas:
        potensi.fasilitas_list = [line.strip() for line in potensi.fasilitas.splitlines() if line.strip()]
    else:
        potensi.fasilitas_list = []

    if potensi.kegiatan_atraksi:
        potensi.kegiatan_atraksi_list = [line.strip() for line in potensi.kegiatan_atraksi.splitlines() if line.strip()]
    else:
        potensi.kegiatan_atraksi_list = []

    if potensi.akomodasi_kuliner_sekitar:
        potensi.akomodasi_kuliner_sekitar_list = [line.strip() for line in potensi.akomodasi_kuliner_sekitar.splitlines() if line.strip()]
    else:
        potensi.akomodasi_kuliner_sekitar_list = []

    if potensi.tips_peringatan:
        potensi.tips_peringatan_list = [line.strip() for line in potensi.tips_peringatan.splitlines() if line.strip()]
    else:
        potensi.tips_peringatan_list = []

    # Untuk SDA
    if potensi.kendala_pengembangan_sda:
        potensi.kendala_pengembangan_sda_list = [line.strip() for line in potensi.kendala_pengembangan_sda.splitlines() if line.strip()]
    else:
        potensi.kendala_pengembangan_sda_list = []

    # Untuk UMKM
    if potensi.legalitas_umkm:
        potensi.legalitas_umkm_list = [line.strip() for line in potensi.legalitas_umkm.splitlines() if line.strip()]
    else:
        potensi.legalitas_umkm_list = []

    if potensi.kontak_umkm_detail:
        potensi.kontak_umkm_detail_list = [line.strip() for line in potensi.kontak_umkm_detail.splitlines() if line.strip()]
    else:
        potensi.kontak_umkm_detail_list = []

    # Untuk Budaya
    if potensi.waktu_tempat_pelaksanaan:
        potensi.waktu_tempat_pelaksanaan_list = [line.strip() for line in potensi.waktu_tempat_pelaksanaan.splitlines() if line.strip()]
    else:
        potensi.waktu_tempat_pelaksanaan_list = []

    if potensi.pelaku_penampil:
        potensi.pelaku_penampil_list = [line.strip() for line in potensi.pelaku_penampil.splitlines() if line.strip()]
    else:
        potensi.pelaku_penampil_list = []

    if potensi.nilai_historis_filosofis:
        potensi.nilai_historis_filosofis_list = [line.strip() for line in potensi.nilai_historis_filosofis.splitlines() if line.strip()]
    else:
        potensi.nilai_historis_filosofis_list = []

    if potensi.upaya_pelestarian:
        potensi.upaya_pelestarian_list = [line.strip() for line in potensi.upaya_pelestarian.splitlines() if line.strip()]
    else:
        potensi.upaya_pelestarian_list = []
    # -----------------------------------------------

    context = {
        'potensi': potensi,
        'gallery_images': gallery_images,
        'title_text': potensi.nama_potensi,
        'description_text': potensi.deskripsi,
    }

    # Logika untuk merender template yang berbeda
    if potensi.jenis_potensi == 'Wisata':
        return render(request, 'wisata_detail.html', context)
    elif potensi.jenis_potensi == 'SDA':
        return render(request, 'sda_detail.html', context)
    elif potensi.jenis_potensi == 'UMKM':
        return render(request, 'umkm_detail.html', context)
    elif potensi.jenis_potensi == 'Budaya':
        return render(request, 'budaya_detail.html', context)
    else:
        # Fallback untuk jenis potensi lain atau yang tidak terdefinisi
        return render(request, 'potensi_umum_detail.html', context) # Buat template ini jika perlu
