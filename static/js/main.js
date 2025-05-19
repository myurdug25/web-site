document.addEventListener('DOMContentLoaded', function() {
    // AOS Animasyon Kütüphanesi Başlatma
    AOS.init({
        duration: 1000,
        once: true,
        offset: 100
    });

    // Typed.js ile Yazı Animasyonu
    var typedTextEl = document.querySelector('.typed-text');
    if (typedTextEl) {
        new Typed('.typed-text', {
            strings: ['Junior Developer', 'Uygulama Geliştirici', 'Freelancer'],
            typeSpeed: 100,
            backSpeed: 50,
            backDelay: 2000,
            loop: true
        });
    }

    // Mobil Menü Toggle
    const menuBtn = document.querySelector('.menu-btn');
    const navLinks = document.querySelector('.nav-links');
    const navLinksItems = document.querySelectorAll('.nav-links a');
    if (menuBtn && navLinks) {
        menuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }
    if (navLinks && navLinksItems.length > 0) {
        navLinksItems.forEach(item => {
            item.addEventListener('click', () => {
                navLinks.classList.remove('active');
            });
        });
    }

    // Navbar Scroll Efekti
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(255, 255, 255, 0.95)';
                navbar.style.backdropFilter = 'blur(10px)';
            } else {
                navbar.style.background = 'rgba(255, 255, 255, 0.8)';
                navbar.style.backdropFilter = 'blur(5px)';
            }
        });
    }

    // Proje Filtreleme
    const filterBtns = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');
    if (filterBtns.length > 0 && projectCards.length > 0) {
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Aktif buton sınıfını güncelle
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Projeleri filtrele
                const filter = btn.getAttribute('data-filter');
                projectCards.forEach(card => {
                    if (filter === 'all' || card.getAttribute('data-category') === filter) {
                        card.style.display = 'block';
                        setTimeout(() => {
                            card.style.opacity = '1';
                            card.style.transform = 'scale(1)';
                        }, 100);
                    } else {
                        card.style.opacity = '0';
                        card.style.transform = 'scale(0.8)';
                        setTimeout(() => {
                            card.style.display = 'none';
                        }, 300);
                    }
                });
            });
        });
    }

    // Form Gönderimi
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Gönderiliyor...';
            submitBtn.disabled = true;
            try {
                const formData = new FormData(contactForm);
                const response = await fetch('contact.php', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                if (data.success) {
                    showNotification('Mesajınız başarıyla gönderildi!', 'success');
                    contactForm.reset();
                } else {
                    showNotification('Bir hata oluştu. Lütfen tekrar deneyin.', 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                showNotification('Bir hata oluştu. Lütfen tekrar deneyin.', 'error');
            } finally {
                submitBtn.innerHTML = originalBtnText;
                submitBtn.disabled = false;
            }
        });
    }

    // Bildirim gösterme fonksiyonu
    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
            ${message}
        `;
        document.body.appendChild(notification);
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }

    // Smooth scroll için
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const anchorTarget = this.getAttribute('href');
            if (window.location.pathname !== "/") {
                window.location.href = "/" + anchorTarget;
                return;
            }
            if (document.querySelector(anchorTarget)) {
                e.preventDefault();
                document.querySelector(anchorTarget).scrollIntoView({
                    behavior: 'smooth'
                });
                setTimeout(() => {
                    history.replaceState(null, '', window.location.pathname);
                }, 500);
            }
        });
    });

    // Kod kopyalama fonksiyonu
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const codeId = btn.getAttribute('data-code');
            const codeElement = document.getElementById(codeId);
            const codeText = codeElement.textContent;
            navigator.clipboard.writeText(codeText).then(() => {
                btn.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => {
                    btn.innerHTML = '<i class="far fa-copy"></i>';
                }, 2000);
            });
        });
    });

    // Kod kategorileri ve alt kategoriler için event listener'lar
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const category = btn.getAttribute('data-category');
            document.querySelectorAll('.code-section').forEach(section => {
                section.classList.remove('active');
                if (section.getAttribute('data-category') === category) {
                    section.classList.add('active');
                }
            });
        });
    });
    document.querySelectorAll('.subcategory-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const parent = btn.closest('.code-section');
            parent.querySelectorAll('.subcategory-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const subcategory = btn.getAttribute('data-subcategory');
            parent.querySelectorAll('.code-grid').forEach(grid => {
                grid.classList.remove('active');
                if (grid.getAttribute('data-subcategory') === subcategory) {
                    grid.classList.add('active');
                }
            });
        });
    });

    // Accordion işlevselliği
    document.querySelectorAll('.accordion-header').forEach(header => {
        header.addEventListener('click', () => {
            const accordion = header.parentElement;
            const isActive = accordion.classList.contains('active');
            
            // Diğer tüm açık accordion'ları kapat
            document.querySelectorAll('.code-accordion').forEach(acc => {
                acc.classList.remove('active');
                const toggle = acc.querySelector('.accordion-toggle i');
                toggle.className = 'fas fa-plus';
            });

            // Tıklanan accordion'u aç/kapat
            if (!isActive) {
                accordion.classList.add('active');
                const toggle = accordion.querySelector('.accordion-toggle i');
                toggle.className = 'fas fa-plus';
            }
        });
    });

    // Detayları Gör butonlarının yeni sekmede açılmasını engelle
    document.querySelectorAll('.btn-outline-primary').forEach(function(link) {
        link.removeAttribute('target');
    });

    document.querySelectorAll('.btn-link').forEach(function(link) {
        link.removeAttribute('target');
    });
}); 