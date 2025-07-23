from django.contrib import admin
from .models import Pengaduan, UMKM, APBDesa, DetailAPBDesa, Article, PotensiDesa # Impor semua model Anda

admin.site.register(Pengaduan)
admin.site.register(UMKM)
admin.site.register(APBDesa)
admin.site.register(DetailAPBDesa)
admin.site.register(Article)
admin.site.register(PotensiDesa) # Daftarkan model PotensiDesa