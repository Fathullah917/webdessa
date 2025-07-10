// JavaScript untuk mengaktifkan/menonaktifkan menu hamburger
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.getElementById('hamburger-icon');
    const navMenu = document.getElementById('main-nav');

    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });

        document.querySelectorAll('#main-nav a').forEach(link => {
            link.addEventListener('click', () => {
                if (navMenu.classList.contains('active')) {
                    navMenu.classList.remove('active');
                }
            });
        });
    } else {
        console.warn("Hamburger icon or navigation menu not found. Mobile navigation might not work correctly.");
    }

    // Inisialisasi Swiper untuk Hero Section dan Articles Section
    // (Kode inisialisasi Swiper kini ada di home.html karena lebih spesifik ke halaman itu)
    // Pastikan Anda telah menyertakan Swiper JS CDN di base.html
});