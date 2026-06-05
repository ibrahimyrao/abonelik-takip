from django.contrib import admin
from .models import Subscription, CreditCard


@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('card_name', 'last_four', 'user', 'created_at')
    list_filter = ('user',)
    search_fields = ('card_name', 'last_four')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'billing_cycle', 'renewal_date',
                    'credit_card', 'category', 'is_active', 'cancelled_at', 'user')
    list_filter = ('billing_cycle', 'category', 'is_active', 'credit_card', 'user')
    search_fields = ('name', 'notes')
    list_editable = ('is_active',)
    date_hierarchy = 'renewal_date'


# Admin site customization
admin.site.site_header = 'Abonelik Takip Yönetimi'
admin.site.site_title = 'Abonelik Takip'
admin.site.index_title = 'Yönetim Paneli'
