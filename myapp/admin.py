# myapp/admin.py
from django.contrib import admin
from .models import Pengaduan, UMKM, APBDesa, DetailAPBDesa, Article # Tambahkan Article

admin.site.register(Pengaduan)
admin.site.register(UMKM)
admin.site.register(APBDesa)
admin.site.register(DetailAPBDesa)
admin.site.register(Article) 