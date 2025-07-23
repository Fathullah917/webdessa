// JavaScript untuk mengaktifkan/menonaktifkan menu hamburger dan mengelola dropdown
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.getElementById('hamburger-icon');
    const navMenu = document.getElementById('main-nav');

    // --- Fungsionalitas Hamburger Menu ---
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            navMenu.classList.toggle('nav-open'); // Menggunakan kelas 'nav-open' sesuai CSS
            // Mengganti ikon hamburger
            const icon = hamburger.querySelector('i');
            if (navMenu.classList.contains('nav-open')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times'); // Ganti ke ikon 'X'
                // Saat menu hamburger dibuka, pastikan semua dropdown tertutup
                closeAllDropdowns();
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars'); // Kembali ke ikon 'burger'
            }
        });

        // Menutup menu saat salah satu item navigasi diklik (termasuk item dropdown child)
        document.querySelectorAll('#main-nav a').forEach(link => {
            link.addEventListener('click', (e) => {
                // Jika ini adalah link parent dari dropdown (contoh: "Potensi Desa") di mobile,
                // jangan tutup menu utama, biarkan dropdown itu sendiri yang di-toggle.
                // Jika itu adalah link child dari dropdown (contoh: "Wisata", "Budaya"), tutup menu utama.
                if (window.innerWidth <= 992 && link.closest('.dropdown')) {
                    const parentLi = link.closest('.dropdown');
                    if (parentLi.querySelector('.dropdown-content') === e.target.nextElementSibling) {
                        // Ini adalah link parent dropdown, biarkan logika dropdown yang menanganinya
                        // Tidak perlu tutup navMenu di sini
                    } else {
                        // Ini adalah link child dari dropdown, tutup navMenu
                        if (navMenu.classList.contains('nav-open')) {
                            navMenu.classList.remove('nav-open');
                            hamburger.querySelector('i').classList.remove('fa-times');
                            hamburger.querySelector('i').classList.add('fa-bars');
                        }
                    }
                } else if (navMenu.classList.contains('nav-open')) {
                    // Jika bukan dropdown parent, dan menu utama terbuka, tutup menu utama
                    navMenu.classList.remove('nav-open');
                    hamburger.querySelector('i').classList.remove('fa-times');
                    hamburger.querySelector('i').classList.add('fa-bars');
                }
            });
        });


        // Menutup menu jika mengklik di luar area navigasi (khusus mobile)
        document.addEventListener('click', (event) => {
            // Periksa jika lebar jendela adalah mobile dan menu nav-open
            if (window.innerWidth <= 992 && navMenu.classList.contains('nav-open')) {
                // Periksa apakah klik berada di luar navMenu dan di luar hamburger
                if (!navMenu.contains(event.target) && !hamburger.contains(event.target)) {
                    navMenu.classList.remove('nav-open');
                    hamburger.querySelector('i').classList.remove('fa-times');
                    hamburger.querySelector('i').classList.add('fa-bars');
                    closeAllDropdowns(); // Tutup juga dropdown jika ada yang terbuka
                }
            }
        });

    } else {
        console.warn("Hamburger icon or navigation menu not found. Mobile navigation might not work correctly.");
    }

    // --- Fungsionalitas Dropdown (untuk Potensi Desa) ---
    const dropdownNav = document.querySelector('nav .dropdown');
    if (dropdownNav) {
        const dropdownContent = dropdownNav.querySelector('.dropdown-content');
        const dropdownLinkParent = dropdownNav.querySelector('.dropdown-toggle'); // The <a> tag that acts as a toggle
        let timeout; // Untuk delay hover di desktop

        // Fungsi bantu untuk menutup semua dropdown
        function closeAllDropdowns() {
            document.querySelectorAll('.dropdown-content').forEach(content => {
                if (content.style.display === 'block') {
                    content.style.opacity = '0';
                    setTimeout(() => content.style.display = 'none', 300);
                }
            });
        }

        // Desktop hover functionality
        dropdownNav.addEventListener('mouseenter', () => {
            // Hanya aktifkan hover di desktop view
            if (window.innerWidth > 992) {
                clearTimeout(timeout);
                closeAllDropdowns(); // Tutup dropdown lain sebelum membuka yang ini
                dropdownContent.style.display = 'block';
                setTimeout(() => dropdownContent.style.opacity = '1', 10);
            }
        });

        dropdownNav.addEventListener('mouseleave', () => {
            // Hanya aktifkan hover di desktop view
            if (window.innerWidth > 992) {
                timeout = setTimeout(() => {
                    dropdownContent.style.opacity = '0';
                    setTimeout(() => dropdownContent.style.display = 'none', 300);
                }, 100);
            }
        });

        // Mobile/Touch device click functionality (toggle)
        dropdownLinkParent.addEventListener('click', (e) => {
            // Hanya aktifkan toggle pada klik di mobile view (atau jika menu hamburger terbuka)
            if (window.innerWidth <= 992) {
                e.preventDefault(); // Mencegah link parent navigasi ke '#'
                // Toggle display dropdownContent
                if (dropdownContent.style.display === 'block') {
                    dropdownContent.style.opacity = '0';
                    setTimeout(() => dropdownContent.style.display = 'none', 300);
                } else {
                    closeAllDropdowns(); // Tutup dropdown lain sebelum membuka yang ini
                    dropdownContent.style.display = 'block';
                    setTimeout(() => dropdownContent.style.opacity = '1', 10);
                }
            }
        });

        // Menutup dropdown jika mengklik di luar area dropdown (khusus untuk desktop jika dibuka dengan klik)
        // Ini jarang dibutuhkan jika hover sudah diterapkan dengan benar, tapi bisa membantu jika ada masalah UX
        document.addEventListener('click', (event) => {
            if (window.innerWidth > 992 && dropdownContent.style.display === 'block') {
                if (!dropdownNav.contains(event.target)) {
                    closeAllDropdowns();
                }
            }
        });
    }

    // --- Inisialisasi Swiper (Jika Ada) ---
    // Pastikan Anda sudah memuat file JS Swiper di base.html
    if (typeof Swiper !== 'undefined') { // Periksa apakah Swiper global ada
        const articlesSwiper = new Swiper('.articles-swiper-container', {
            slidesPerView: 1,
            spaceBetween: 30,
            loop: true,
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            breakpoints: {
                640: {
                    slidesPerView: 2,
                    spaceBetween: 20,
                },
                1024: {
                    slidesPerView: 3,
                    spaceBetween: 30,
                },
            },
            autoplay: {
                delay: 5000, // Otomatis geser setiap 5 detik
                disableOnInteraction: false, // Lanjutkan autoplay setelah interaksi pengguna
            },
        });
    } else {
        console.warn("Swiper library not found. Article carousel might not function.");
    }

    // --- Fungsionalitas Scroll-to-Top (Opsional, jika Anda punya tombolnya) ---
    const scrollTopButton = document.getElementById('scroll-top-button');
    if (scrollTopButton) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) { // Tampilkan setelah scroll 300px
                scrollTopButton.style.display = 'block';
            } else {
                scrollTopButton.style.display = 'none';
            }
        });

        scrollTopButton.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
});