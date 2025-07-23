from django.shortcuts import render, get_object_or_404
from django.utils import timezone # Ditambahkan untuk filter tanggal
from datetime import timedelta   # Ditambahkan untuk filter tanggal

# Impor semua model yang relevan
from .models import Pengaduan, UMKM, APBDesa, DetailAPBDesa, Article, PotensiDesa

# ... (impor lainnya)

from django.shortcuts import render
from .models import Article # Tidak perlu Category lagi jika filter diubah
from datetime import datetime, timedelta
from django.utils import timezone # Penting untuk zona waktu Django

def home_view(request):
    articles = Article.objects.all().order_by('-created_at') # Ambil semua artikel

    selected_time_period = request.GET.get('time_period')

    if selected_time_period:
        now = timezone.now()

        if selected_time_period == 'today':
            articles = articles.filter(created_at__date=now.date())
        elif selected_time_period == 'this_week':
            # Untuk 'minggu ini', hitung dari hari Senin minggu ini
            start_of_week = now - timedelta(days=now.weekday())
            articles = articles.filter(created_at__gte=start_of_week.date())
        elif selected_time_period == 'this_month':
            articles = articles.filter(created_at__year=now.year, created_at__month=now.month)
        elif selected_time_period == 'this_year':
            articles = articles.filter(created_at__year=now.year)

    # Batasi jumlah artikel yang ditampilkan di beranda (misalnya, 12 artikel untuk carousel)
    # Anda perlu artikel yang cukup banyak agar carousel bisa digeser dan terlihat efeknya.
    # Jika Anda hanya memiliki 3 artikel, loop:true akan bekerja, tapi tidak akan ada geseran "baru".
    # Pastikan jumlah ini lebih besar dari slidesPerView * 2 atau lebih untuk efek loop yang baik.
    articles = articles[:12] # Mengambil hingga 12 artikel (misal: 4 grup x 3 slide)

    context = {
        'articles': articles,
        'selected_time_period': selected_time_period,
    }
    return render(request, 'home.html', context)
# --- Article List View (Menampilkan semua artikel dengan filter) ---
def article_list_view(request):
    # Dapatkan parameter filter dari URL (misal: /berita/?filter=this_month)
    filter_option = request.GET.get('filter', 'all') # Default ke 'all'

    articles = Article.objects.all().order_by('-created_at')

    # Logika filter
    if filter_option == 'this_week':
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday()) # Monday as start of week
        end_of_week = start_of_week + timedelta(days=6)
        articles = articles.filter(created_at__date__range=[start_of_week, end_of_week])
    elif filter_option == 'this_month':
        today = timezone.now().date()
        articles = articles.filter(created_at__year=today.year, created_at__month=today.month)
    elif filter_option == 'this_year':
        today = timezone.now().date()
        articles = articles.filter(created_at__year=today.year)
    # Jika filter_option adalah 'all' atau tidak dikenali, semua artikel akan ditampilkan

    context = {
        'all_articles': articles,
        'page_title': 'Semua Berita & Artikel',
        'active_filter': filter_option # Kirim filter yang aktif ke template
    }
    return render(request, 'article_list.html', context)

# --- Article Detail View ---
def article_detail_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    context = {
        'article': article,
        'page_title': article.title # Tambahkan page_title agar konsisten
    }
    return render(request, 'artikel_detail.html', context)


# --- Pengaduan Views ---
def pengaduan_view(request):
    return render(request, 'pengaduan.html')

def daftar_pengaduan_publik_view(request):
    public_pengaduans = Pengaduan.objects.filter(status_pengaduan__in=['Dalam Proses', 'Selesai']).order_by('-tanggal_pengaduan')
    context = {
        'public_pengaduans': public_pengaduans
    }
    return render(request, 'daftar_pengaduan_publik.html', context)


# --- UMKM View ---
def umkm_potensi_view(request):
    umkm_list = UMKM.objects.all().order_by('nama_umkm')

    for i, umkm in enumerate(umkm_list):
        umkm.animation_delay = (i + 1) * 0.1

    context = {
        'umkm_list': umkm_list,
        'title_text': 'UMKM Desa Boyemare',
        'description_text': 'Daftar Usaha Mikro, Kecil, dan Menengah (UMKM) yang berkembang di Desa Boyemare. Dukung produk lokal kami!'
    }
    return render(request, 'umkm.html', context)

# --- APBDesa Views ---
def apbdesa_view(request):
    apbdesa_data = APBDesa.objects.all().order_by('-tahun')
    context = {
        'apbdesa_data': apbdesa_data
    }
    return render(request, 'dataAPBDes.html', context)

def detail_apbdesa_view(request, tahun):
    apbdesa = get_object_or_404(APBDesa, tahun=tahun)
    detail_items = apbdesa.details.all()
    context = {
        'apbdesa': apbdesa,
        'detail_items': detail_items,
    }
    return render(request, 'detail_apbdesa.html', context)

# --- About Us View ---
def about_view(request):
    return render(request, 'about.html')

# --- Potensi Desa Views ---

def potensi_desa_index_view(request):
    all_potensi = PotensiDesa.objects.all().order_by('-tanggal_publikasi')

    # --- DEBUGGING PRINTS ---
    # print("\n--- DEBUG: potensi_desa_index_view ---")
    # print(f"Jumlah Potensi Desa yang diambil: {all_potensi.count()}")
    # if not all_potensi.exists():
    #     print("PERHATIAN: Query all_potensi menghasilkan 0 objek. Pastikan ada data di database.")
    for i, potensi in enumerate(all_potensi):
        # print(f"  Potensi {i+1}: Nama={potensi.nama_potensi}, Jenis={potensi.jenis_potensi}, PK={potensi.pk}, Delay={getattr(potensi, 'animation_delay', 'belum dihitung')}")
        potensi.animation_delay = (i + 1) * 0.1 # Pastikan ini di sini setelah print
        # print(f"    Setelah hitung delay: Delay={potensi.animation_delay}")
    # print("--- END DEBUG ---\n")
    # --- END DEBUGGING ---

    context = {
        'potensi_list': all_potensi,
        'title_text': 'Semua Potensi Desa Boyemare',
        'description_text': 'Jelajahi berbagai potensi yang ada di Desa Boyemare, mulai dari wisata, pertanian, budaya, hingga UMKM lokal.'
    }
    return render(request, 'potensi_desa.html', context)


def wisata_view(request):
    wisata_list = PotensiDesa.objects.filter(jenis_potensi='Wisata').order_by('-tanggal_publikasi')

    # --- DEBUGGING PRINTS ---
    # print("\n--- DEBUG: wisata_view ---")
    # print(f"Jumlah Potensi Wisata yang diambil: {wisata_list.count()}")
    # if not wisata_list.exists():
    #     print("PERHATIAN: Query wisata_list menghasilkan 0 objek. Pastikan ada data 'Wisata' di database.")
    for i, potensi in enumerate(wisata_list):
        # print(f"  Wisata {i+1}: Nama={potensi.nama_potensi}, Jenis={potensi.jenis_potensi}, PK={potensi.pk}, Delay={getattr(potensi, 'animation_delay', 'belum dihitung')}")
        potensi.animation_delay = (i + 1) * 0.1
        # print(f"    Setelah hitung delay: Delay={potensi.animation_delay}")
    # print("--- END DEBUG ---\n")
    # --- END DEBUGGING ---

    context = {
        'potensi_list': wisata_list,
        'title_text': 'Wisata Desa Boyemare',
        'description_text': 'Jelajahi destinasi wisata alam dan budaya yang menawan di Desa Boyemare. Temukan keindahan tersembunyi dan pengalaman tak terlupakan yang ditawarkan oleh desa kami.'
    }
    return render(request, 'wisata.html', context)

def pertanian_view(request):
    pertanian_list = PotensiDesa.objects.filter(jenis_potensi='Pertanian').order_by('-tanggal_publikasi')

    for i, potensi in enumerate(pertanian_list):
        potensi.animation_delay = (i + 1) * 0.1

    context = {
        'potensi_list': pertanian_list,
        'title_text': 'Potensi Pertanian Desa Boyemare',
        'description_text': 'Informasi seputar hasil pertanian unggulan, inovasi petani lokal, dan program-program yang mendukung sektor pertanian di Desa Boyemare. Sumber pangan lokal dan ekonomi berkelanjutan.'
    }
    return render(request, 'pertanian.html', context)

def budaya_view(request):
    budaya_list = PotensiDesa.objects.filter(jenis_potensi='Budaya').order_by('-tanggal_publikasi')

    for i, potensi in enumerate(budaya_list):
        potensi.animation_delay = (i + 1) * 0.1

    context = {
        'potensi_list': budaya_list,
        'title_text': 'Seni & Budaya Desa Boyemare',
        'description_text': 'Jelajahi kekayaan seni tradisional, adat istiadat, upacara, dan warisan budaya yang dijunjung tinggi di Desa Boyemare. Pelajari lebih lanjut tentang identitas dan tradisi kami.'
    }
    return render(request, 'budaya.html', context)

def potensi_desa_detail_view(request, pk):
    potensi = get_object_or_404(PotensiDesa, pk=pk)
    context = {
        'potensi': potensi,
        'title_text': potensi.nama_potensi,
        'description_text': potensi.deskripsi[:150] # Ambil 150 karakter pertama untuk deskripsi
    }
    return render(request, 'potensi_desa_detail.html', context)