from django.db import models
from django.contrib.auth.models import User


class CreditCard(models.Model):
    """Kullanıcının kredi kartları."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credit_cards')
    card_name = models.CharField(max_length=100, verbose_name='Kart Adı',
                                  help_text='Örn: Ziraat Bankası Visa')
    last_four = models.CharField(max_length=4, verbose_name='Son 4 Hane')
    card_color = models.CharField(max_length=7, default='#6366f1', verbose_name='Kart Rengi',
                                   help_text='HEX renk kodu (örn: #6366f1)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Kredi Kartı'
        verbose_name_plural = 'Kredi Kartları'
        ordering = ['card_name']

    def __str__(self):
        return f"{self.card_name} (****{self.last_four})"


class Subscription(models.Model):
    """Kullanıcının abonelikleri."""
    BILLING_CHOICES = [
        ('monthly', 'Aylık'),
        ('yearly', 'Yıllık'),
    ]
    CATEGORY_CHOICES = [
        ('muzik', 'Müzik'),
        ('video', 'Video & Streaming'),
        ('oyun', 'Oyun'),
        ('bulut', 'Bulut Depolama'),
        ('yazilim', 'Yazılım'),
        ('egitim', 'Eğitim'),
        ('haber', 'Haber & Dergi'),
        ('saglik', 'Sağlık & Fitness'),
        ('diger', 'Diğer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    name = models.CharField(max_length=200, verbose_name='Abonelik Adı')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ücret (₺)')
    billing_cycle = models.CharField(max_length=10, choices=BILLING_CHOICES,
                                      default='monthly', verbose_name='Ödeme Periyodu')
    renewal_date = models.DateField(verbose_name='Sonraki Ödeme Tarihi')
    credit_card = models.ForeignKey(CreditCard, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='subscriptions',
                                     verbose_name='Kredi Kartı')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES,
                                 default='diger', verbose_name='Kategori')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    cancelled_at = models.DateField(null=True, blank=True, verbose_name='İptal Tarihi')
    notes = models.TextField(blank=True, verbose_name='Notlar')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Abonelik'
        verbose_name_plural = 'Abonelikler'
        ordering = ['renewal_date']

    def __str__(self):
        return f"{self.name} — {self.price}₺/{self.get_billing_cycle_display()}"

    @property
    def monthly_cost(self):
        """Aylık maliyeti hesapla."""
        if self.billing_cycle == 'yearly':
            return round(self.price / 12, 2)
        return self.price
