# 💳 Abonelik Takip Sistemi

Modern, şık ve Docker tabanlı bir abonelik ve gider takip uygulaması. Django frameworkü ile geliştirilmiş olup, kredi kartı bazlı ödeme takibi ve kategorize edilmiş abonelik giderlerinizi izlemenizi sağlar.

---

## ✨ Özellikler

*   **💳 Kredi Kartı Yönetimi:** Kartlarınıza özel tanımlayıcı isimler, son 4 hane bilgisi ve görsel ayrıştırma için özelleştirilmiş HEX renkleri belirleyin.
*   **📅 Abonelik Planlama:** Aylık veya yıllık ödeme periyotları, yenilenme tarihleri ve aktif/pasif durum takibi.
*   **📊 Gider Analizi:** Kategorilere göre filtrelenmiş (Müzik, Video, Bulut Depolama, Oyun, Yazılım vb.) aylık ortalama maliyet hesaplamaları.
*   **🔒 Üst Düzey Güvenlik:** Django'nun yerleşik CSRF, XSS koruması, güvenli cookie yapılandırması ve kullanıcı girişi zorunluluğu.
*   **🐳 Docker Desteği:** Docker ve Docker Compose ile tek komutla ayağa kaldırılabilen mimari.
*   **⚡ Statik Dosya Optimizasyonu:** WhiteNoise entegrasyonu ile hızlı statik dosya sunumu.

---

## 🛠️ Teknoloji Yığını

*   **Backend:** Python 3 + Django 5+
*   **Veritabanı:** SQLite (Geliştirme ve küçük ölçekli kullanım için ideal)
*   **Sunucu & Statik:** Gunicorn + WhiteNoise
*   **Konteynerleştirme:** Docker & Docker Compose

---

## 🚀 Hızlı Başlangıç

### 1. Yerel Kurulum (Geliştirme Ortamı)

**Gereksinimler:** Python 3.10+, pip, virtualenv

1.  **Projeyi Kopyalayın:**
    ```bash
    git clone https://github.com/KULLANICI_ADINIZ/abonelik-takip.git
    cd abonelik-takip
    ```

2.  **Sanal Ortam Oluşturun ve Aktifleştirin:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Windows için: venv\Scripts\activate
    ```

3.  **Bağımlılıkları Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ortam Değişkenlerini Yapılandırın:**
    `.env.example` dosyasını `.env` olarak kopyalayın ve düzenleyin:
    ```bash
    cp .env.example .env
    ```
    `.env` içeriğini kendinize göre güncelleyin (özellikle `SECRET_KEY` ve `ALLOWED_HOSTS`).

5.  **Veritabanını Hazırlayın:**
    ```bash
    python manage.py migrate
    ```

6.  **Yönetici Kullanıcısı (Superuser) Oluşturun:**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Projeyi Çalıştırın:**
    ```bash
    python manage.py runserver
    ```
    Uygulamaya tarayıcınızdan `http://127.0.0.1:8000` adresinden erişebilirsiniz.

---

### 🐳 2. Docker ile Çalıştırma (Önerilen)

Docker kurulu olan her sistemde projeyi tek komutla çalıştırabilirsiniz:

1.  **Ağaç Yapısını Derleyin ve Başlatın:**
    ```bash
    docker compose up -d --build
    ```

2.  **Veritabanı Tablolarını Oluşturun:**
    ```bash
    docker compose exec web python manage.py migrate
    ```

3.  **Yönetici Kullanıcısı Oluşturun:**
    ```bash
    docker compose exec web python manage.py createsuperuser
    ```

Uygulama varsayılan olarak **8084** portunda çalışacaktır (`http://localhost:8084`).

---

## 🔒 Güvenlik ve Canlıya Alma (Production)

Bu proje Raspberry Pi, bulut sunucular veya kişisel sunucularda kolayca deploy edilmek üzere tasarlanmıştır. Detaylı canlı ortam kurulum adımları, Cloudflare Tunnel ayarları ve güvenlik önlemleri için [DEPLOYMENT.md](file:///Users/ibrahimyalcinridvanagaoglu/Desktop/Kodlar/abonelik-takip/DEPLOYMENT.md) dosyasını inceleyebilirsiniz.

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına göz atabilirsiniz.
