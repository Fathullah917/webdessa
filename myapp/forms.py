from django import forms
from .models import Pengaduan

class PengaduanForm(forms.ModelForm):
    class Meta:
        model = Pengaduan
        fields = [
            'nama_pelapor',
            'email_pelapor',
            'nomor_telepon',
            'jenis_pengaduan',
            'judul_pengaduan',
            'isi_pengaduan',
            'bukti_foto'
        ]
        widgets = {
            'isi_pengaduan': forms.Textarea(attrs={'rows': 5}),
            'nama_pelapor': forms.TextInput(attrs={'placeholder': 'Masukkan nama Anda'}),
            'email_pelapor': forms.EmailInput(attrs={'placeholder': 'Masukkan email Anda (opsional)'}),
            'nomor_telepon': forms.TextInput(attrs={'placeholder': 'Masukkan nomor telepon (opsional)'}),
            'judul_pengaduan': forms.TextInput(attrs={'placeholder': 'Ringkasan singkat pengaduan Anda'}),
        }
        labels = {
            'nama_pelapor': 'Nama Lengkap',
            'email_pelapor': 'Email',
            'nomor_telepon': 'Nomor Telepon/HP',
            'jenis_pengaduan': 'Jenis Pengaduan',
            'judul_pengaduan': 'Judul Pengaduan',
            'isi_pengaduan': 'Detail Pengaduan',
            'bukti_foto': 'Unggah Bukti Foto',
        }