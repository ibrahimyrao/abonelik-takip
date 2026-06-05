# 🚀 Deployment Rehberi — Abonelik Takip

Bu rehber Raspberry Pi 5 (CasaOS) üzerinde Docker ile deployment ve Cloudflare Tunnel ile dış erişim kurulumunu açıklar.

---

## 1. Raspberry Pi 5 Kurulumu

### Ön Gereksinimler
- CasaOS yüklü Raspberry Pi 5
- Docker & Docker Compose yüklü (`casaos` ile birlikte gelir)
- Git yüklü

### Projeyi RPi'ye Kopyalama

```bash
# RPi'ya SSH ile bağlan
ssh kullanici@<RPi-IP>

# Proje dizinine git
cd /DATA/AppData  # veya tercih ettiğin dizin

# Projeyi kopyala
git clone <REPO_URL> abonelik-takip
cd abonelik-takip
```

### Ortam Değişkenlerini Ayarla

```bash
# .env dosyası oluştur
cp .env.example .env

# Güçlü bir SECRET_KEY oluştur
python3 -c "import secrets; print(secrets.token_urlsafe(50))"

# .env dosyasını düzenle
nano .env
```

`.env` içeriği:
```
SECRET_KEY=<yukarida-olusturdugun-key>
DEBUG=0
ALLOWED_HOSTS=abonelik.yourdomain.com,your-local-ip
CSRF_TRUSTED_ORIGINS=https://abonelik.yourdomain.com
```

### Docker ile Başlatma

```bash
# Build ve başlat
docker compose up -d --build

# Veritabanı migration
docker compose exec web python manage.py migrate

# Admin kullanıcı oluştur
docker compose exec web python manage.py createsuperuser

# Logları kontrol et
docker compose logs -f web
```

Uygulama artık `http://<RPi-IP>:8084` adresinde çalışıyor.

---

## 2. Cloudflare Tunnel Kurulumu

### Mevcut Tunnel'a Yeni Hostname Ekleme

Zaten `diger-uygulama.yourdomain.com` için bir tunnel kurulmuşsa:

1. **Cloudflare Dashboard** → Zero Trust → Networks → Tunnels
2. Mevcut tunnel'ı seç → **Configure**
3. **Public Hostnames** → **Add a public hostname**:
   - **Subdomain**: `abonelik`
   - **Domain**: `yourdomain.com`
   - **Type**: `HTTP`
   - **URL**: `your-local-ip:8084`
4. Kaydet

### Yeni Tunnel Kurulumu (ilk kez ise)

```bash
# cloudflared yükle
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 -o /usr/local/bin/cloudflared
chmod +x /usr/local/bin/cloudflared

# Login
cloudflared tunnel login

# Tunnel oluştur
cloudflared tunnel create abonelik-takip

# Config dosyası
cat > ~/.cloudflared/config.yml << EOF
tunnel: <TUNNEL-ID>
credentials-file: /root/.cloudflared/<TUNNEL-ID>.json

ingress:
  - hostname: abonelik.yourdomain.com
    service: http://your-local-ip:8084
  - service: http_status:404
EOF

# DNS kaydı ekle
cloudflared tunnel route dns <TUNNEL-ID> abonelik.yourdomain.com

# Başlat
cloudflared tunnel run
```

### Servis Olarak Çalıştırma

```bash
cloudflared service install
systemctl enable cloudflared
systemctl start cloudflared
```

---

## 3. Cloudflare Zero Trust / Access (Önerilen)

Uygulamayı sadece sana özel yapmak için Cloudflare Access kullanabilirsin:

1. **Cloudflare Dashboard** → Zero Trust → Access → Applications
2. **Add an application** → Self-hosted
3. Ayarlar:
   - **Application name**: Abonelik Takip
   - **Session duration**: 24 hours
   - **Application domain**: `abonelik.yourdomain.com`
4. **Policy** oluştur:
   - **Policy name**: Only Me
   - **Action**: Allow
   - **Include**: Emails → `your-email@example.com`
5. Kaydet

Bu sayede uygulama iki katmanlı güvenliğe sahip olur:
- ✅ Cloudflare Access (email doğrulama)
- ✅ Django Login (kullanıcı adı + şifre)

---

## 4. Güvenlik Best Practices

### Django Güvenlik Ayarları (Zaten Aktif)
- ✅ `DEBUG = False` (production'da)
- ✅ Güçlü `SECRET_KEY` (.env'den okunur)
- ✅ `CSRF_COOKIE_SECURE = True`
- ✅ `SESSION_COOKIE_SECURE = True`
- ✅ `SECURE_PROXY_SSL_HEADER` (Cloudflare proxy)
- ✅ `X_FRAME_OPTIONS = 'DENY'`
- ✅ `SECURE_CONTENT_TYPE_NOSNIFF = True`
- ✅ `SECURE_BROWSER_XSS_FILTER = True`
- ✅ `@login_required` tüm görünümlerde
- ✅ CSRF koruması tüm formlarda

### Ek Öneriler
- 🔐 SSH key-based authentication kullan (RPi erişimi için)
- 🔐 `fail2ban` kur (SSH brute-force koruması)
- 🔐 Firewall'ı yapılandır: sadece 22 (SSH) ve 8084 (uygulama) açık olsun
- 🔐 Düzenli yedekleme: `db.sqlite3` dosyasını yedekle
- 🔐 Docker imajlarını güncel tut

### Yedekleme Script'i

```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/DATA/backups/abonelik-takip"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
cp /DATA/AppData/abonelik-takip/db.sqlite3 $BACKUP_DIR/db_$DATE.sqlite3
# Eski yedekleri sil (30 günden eski)
find $BACKUP_DIR -name "*.sqlite3" -mtime +30 -delete
```

Crontab'a ekle:
```bash
crontab -e
# Her gün gece 3'te yedekle
0 3 * * * /DATA/scripts/backup.sh
```

---

## 5. Güncelleme

```bash
cd /DATA/AppData/abonelik-takip
git pull
docker compose up -d --build
docker compose exec web python manage.py migrate
```
