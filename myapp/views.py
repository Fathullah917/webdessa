from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages

# Pastikan Anda sudah mengimpor semua model dan form yang diperlukan
from .models import Pengaduan, UMKM, APBDesa, DetailAPBDesa, Article
from .forms import PengaduanForm

# --- Views untuk Halaman Umum ---

def home_view(request):
    # Mengambil semua artikel, diurutkan berdasarkan tanggal pembuatan terbaru
    articles = Article.objects.all().order_by('-created_at')
    context = {'articles': articles}
    return render(request, 'home.html', context)

def about_view(request):
    # Merender halaman "Tentang Kami"
    return render(request, 'about.html')

def dataAPBDes_view(request):
    # Mengambil semua data APBDesa, diurutkan berdasarkan tahun terbaru
    apbdesa_list = APBDesa.objects.all().order_by('-tahun')
    context = {
        'apbdesa_list': apbdesa_list
    }
    return render(request, 'dataAPBDes.html', context)

def umkm_view(request):
    # Mengambil semua data UMKM, diurutkan berdasarkan nama
    umkm_list = UMKM.objects.all().order_by('nama_umkm')
    context = {
        'umkm_list': umkm_list # Pastikan nama variabel konteks ini konsisten dengan yang digunakan di template umkm.html
    }
    return render(request, 'umkm.html', context) # Memanggil template 'umkm.html'

# --- View untuk Form Pengaduan DAN Daftar Pengaduan Publik di halaman yang SAMA ---
def pengaduan_view(request):
    if request.method == 'POST':
        form = PengaduanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Pesan sukses setelah pengaduan terkirim
            messages.success(request, 'Pengaduan Anda berhasil terkirim! Silakan lihat daftar pengaduan di bawah.')
            form = PengaduanForm() # Reset form agar kolom input kembali kosong setelah submit
        else:
            # Pesan error jika form tidak valid
            messages.error(request, 'Terjadi kesalahan pada input Anda. Mohon periksa kembali.')
    else:
        form = PengaduanForm() # Menginisialisasi form kosong untuk request GET

    # --- Logika untuk Daftar Pengaduan dan Statistik Mingguan ---
    # Mengambil semua pengaduan, diurutkan berdasarkan tanggal pengaduan terbaru
    pengaduan_list = Pengaduan.objects.all().order_by('-tanggal_pengaduan')
    
    now = timezone.now()
    one_week_ago = now - timezone.timedelta(days=7) # Menghitung waktu seminggu yang lalu

    # Menghitung jumlah total pengaduan dalam seminggu terakhir
    pengaduan_mingguan = Pengaduan.objects.filter(tanggal_pengaduan__gte=one_week_ago).count()

    # Menghitung jumlah pengaduan berdasarkan status dalam seminggu terakhir
    pengaduan_status_mingguan = {
        'Baru': Pengaduan.objects.filter(
            tanggal_pengaduan__gte=one_week_ago,
            status_pengaduan='Baru'
        ).count(),
        'Dalam_Proses': Pengaduan.objects.filter(
            tanggal_pengaduan__gte=one_week_ago,
            status_pengaduan='Dalam Proses' # PENTING: Pastikan string ini cocok persis dengan pilihan di model Pengaduan
        ).count(),
        'Selesai': Pengaduan.objects.filter(
            tanggal_pengaduan__gte=one_week_ago,
            status_pengaduan='Selesai'
        ).count(),
        'Ditolak': Pengaduan.objects.filter(
            tanggal_pengaduan__gte=one_week_ago,
            status_pengaduan='Ditolak'
        ).count(),
    }
    # -------------------------------------------------------------

    # Menggabungkan semua data ke dalam satu konteks untuk template
    context = {
        'form': form,
        'pengaduan_list': pengaduan_list,
        'pengaduan_mingguan': pengaduan_mingguan,
        'pengaduan_status_mingguan': pengaduan_status_mingguan
    }
    return render(request, 'pengaduan.html', context) # Memanggil template 'pengaduan.html'