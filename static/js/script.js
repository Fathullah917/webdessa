// JavaScript untuk mengaktifkan/menonaktifkan menu hamburger
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.getElementById('hamburger-icon');
    const navMenu = document.getElementById('main-nav');

    // Pastikan elemen ditemukan sebelum menambahkan event listener
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            navMenu.classList.toggle('active'); // Tambah/hapus class 'active'
        });

        // Opsional: Tutup menu saat link diklik (untuk UX yang lebih baik)
        document.querySelectorAll('#main-nav a').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
            });
        });
    } else {
        // Pesan peringatan jika elemen tidak ditemukan (membantu debugging)
        console.warn("Hamburger icon or navigation menu not found. Mobile navigation might not work.");
    }
});