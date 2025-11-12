Django Web Sitesi – README

Bu proje, Django framework kullanılarak geliştirilmiş bir web uygulamasıdır. Proje; modern, ölçeklenebilir ve yönetilebilir bir mimari üzerine kurulmuş olup hem backend hem de admin panel üzerinden içerik yönetimi sunar.

📌 Özellikler

✔️ Django 5.x tabanlı modern web uygulaması

✔️ Admin panel üzerinden içerik yönetimi

✔️ Dinamik sayfalar (Home / About / Contact / Blog vb.)

✔️ Mobil uyumlu (Responsive) tasarım

✔️ Kullanıcı dostu URL yapısı

✔️ Güvenli form işleme ve doğrulama

✔️ Veritabanı ile tam entegrasyon (SQLite/PostgreSQL/MySQL)

✔️ Ortam değişkenleri ile gizli anahtar yönetimi

✔️ Template + Static + Media yapılandırması

🏗 Teknolojiler
Teknoloji	Açıklama
Python	3.10+
Django	4.x / 5.x
HTML / CSS / Bootstrap	Frontend
SQLite / PostgreSQL	Veritabanı
Django ORM	Veri yönetimi
Gunicorn / Nginx (Opsiyonel)	Deployment
📁 Proje Yapısı
project_name/
│
├── project_name/        # Proje ayarları
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── app_name/            # Uygulama dosyaları
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/
│
├── static/              # CSS, JS, resimler
├── media/               # Yüklenen dosyalar
├── requirements.txt
└── manage.py

🚀 Kurulum & Çalıştırma
1️⃣ Projeyi Klonla
git clone https://github.com/kullanici/proje-adi.git
cd proje-adi

2️⃣ Sanal Ortam Oluştur
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3️⃣ Gereksinimleri Kur
pip install -r requirements.txt

4️⃣ Veritabanını Migrat Et
python manage.py migrate

5️⃣ Süper Kullanıcı Oluştur
python manage.py createsuperuser

6️⃣ Projeyi Başlat
python manage.py runserver
