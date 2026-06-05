import calendar
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import timedelta, date
from decimal import Decimal

from .models import Subscription, CreditCard
from .forms import SubscriptionForm, CreditCardForm


@login_required
def dashboard(request):
    """Ana sayfa — dashboard."""
    today = timezone.now().date()
    week_later = today + timedelta(days=7)

    active_subs = Subscription.objects.filter(user=request.user, is_active=True)
    all_subs = Subscription.objects.filter(user=request.user)

    # Yaklaşan ödemeler (7 gün içi)
    upcoming = active_subs.filter(
        renewal_date__gte=today,
        renewal_date__lte=week_later
    ).order_by('renewal_date')

    # Gecikmiş ödemeler
    overdue = active_subs.filter(renewal_date__lt=today).order_by('renewal_date')

    # Toplam aylık harcama
    total_monthly = Decimal('0.00')
    for sub in active_subs:
        total_monthly += sub.monthly_cost

    # Toplam yıllık harcama
    total_yearly = Decimal('0.00')
    for sub in active_subs:
        if sub.billing_cycle == 'yearly':
            total_yearly += sub.price
        else:
            total_yearly += sub.price * 12

    # Kredi kartı bazlı harcama özeti
    cards = CreditCard.objects.filter(user=request.user)
    card_summary = []
    for card in cards:
        card_subs = active_subs.filter(credit_card=card)
        card_monthly = sum(s.monthly_cost for s in card_subs)
        card_summary.append({
            'card': card,
            'subscription_count': card_subs.count(),
            'monthly_total': card_monthly,
        })

    # Kartsız abonelikler
    no_card_subs = active_subs.filter(credit_card__isnull=True)
    if no_card_subs.exists():
        card_summary.append({
            'card': None,
            'subscription_count': no_card_subs.count(),
            'monthly_total': sum(s.monthly_cost for s in no_card_subs),
        })

    # Son eklenen abonelikler
    recent = all_subs.order_by('-created_at')[:5]

    # Kategori dağılımı
    category_data = {}
    for sub in active_subs:
        cat = sub.get_category_display()
        if cat not in category_data:
            category_data[cat] = Decimal('0.00')
        category_data[cat] += sub.monthly_cost

    # Ödeme Takvimi
    cal_month = int(request.GET.get('month', today.month))
    cal_year = int(request.GET.get('year', today.year))
    cal_subs = list(active_subs.values('name', 'renewal_date', 'price', 'category', 'pk'))
    cal = calendar.monthcalendar(cal_year, cal_month)
    cal_weeks = []
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append({'day': None, 'subs': []})
            else:
                d = date(cal_year, cal_month, day)
                day_subs = [s for s in cal_subs if s['renewal_date'] == d]
                week_data.append({
                    'day': day,
                    'date': d,
                    'subs': day_subs,
                    'is_today': d == today,
                    'is_past': d < today,
                })
        cal_weeks.append(week_data)
    prev_month = cal_month - 1 if cal_month > 1 else 12
    prev_year = cal_year if cal_month > 1 else cal_year - 1
    next_month = cal_month + 1 if cal_month < 12 else 1
    next_year = cal_year if cal_month < 12 else cal_year + 1
    month_names = ['', 'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
                   'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']

    context = {
        'upcoming': upcoming,
        'overdue': overdue,
        'recent': recent,
        'all_active': active_subs.order_by('renewal_date'),
        'active_count': active_subs.count(),
        'total_count': all_subs.count(),
        'total_monthly': total_monthly,
        'total_yearly': total_yearly,
        'card_summary': card_summary,
        'category_data': category_data,
        'today': today,
        'cal_weeks': cal_weeks,
        'cal_month': cal_month,
        'cal_year': cal_year,
        'cal_month_name': month_names[cal_month],
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
    }
    return render(request, 'subscriptions/dashboard.html', context)


@login_required
def subscription_add(request):
    """Yeni abonelik ekle."""
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, user=request.user)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.user = request.user
            sub.save()
            messages.success(request, f'"{sub.name}" aboneliği eklendi.')
            return redirect('dashboard')
    else:
        form = SubscriptionForm(user=request.user)
    return render(request, 'subscriptions/subscription_form.html', {
        'form': form,
        'title': 'Yeni Abonelik Ekle',
        'button_text': 'Ekle',
    })


@login_required
def subscription_edit(request, pk):
    """Abonelik düzenle."""
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=sub, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{sub.name}" güncellendi.')
            return redirect('dashboard')
    else:
        form = SubscriptionForm(instance=sub, user=request.user)
    return render(request, 'subscriptions/subscription_form.html', {
        'form': form,
        'title': f'Düzenle: {sub.name}',
        'button_text': 'Güncelle',
        'subscription': sub,
    })


@login_required
def subscription_delete(request, pk):
    """Abonelik sil."""
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == 'POST':
        name = sub.name
        sub.delete()
        messages.success(request, f'"{name}" silindi.')
        return redirect('dashboard')
    return render(request, 'subscriptions/subscription_confirm_delete.html', {
        'subscription': sub,
    })


@login_required
def card_list(request):
    """Kredi kartları listesi."""
    cards = CreditCard.objects.filter(user=request.user)
    return render(request, 'subscriptions/card_list.html', {'cards': cards})


@login_required
def card_add(request):
    """Yeni kredi kartı ekle."""
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            messages.success(request, f'"{card.card_name}" kartı eklendi.')
            return redirect('card_list')
    else:
        form = CreditCardForm()
    return render(request, 'subscriptions/card_form.html', {
        'form': form,
        'title': 'Yeni Kart Ekle',
        'button_text': 'Ekle',
    })


@login_required
def card_edit(request, pk):
    """Kredi kartı düzenle."""
    card = get_object_or_404(CreditCard, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CreditCardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{card.card_name}" güncellendi.')
            return redirect('card_list')
    else:
        form = CreditCardForm(instance=card)
    return render(request, 'subscriptions/card_form.html', {
        'form': form,
        'title': f'Düzenle: {card.card_name}',
        'button_text': 'Güncelle',
        'card': card,
    })


@login_required
def card_delete(request, pk):
    """Kredi kartı sil."""
    card = get_object_or_404(CreditCard, pk=pk, user=request.user)
    if request.method == 'POST':
        name = card.card_name
        card.delete()
        messages.success(request, f'"{name}" kartı silindi.')
        return redirect('card_list')
    return render(request, 'subscriptions/card_confirm_delete.html', {
        'card': card,
    })


@login_required
def subscription_list(request):
    """Abonelik listesi + filtreleme/arama."""
    subs = Subscription.objects.filter(user=request.user)

    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    billing = request.GET.get('billing', '')
    status = request.GET.get('status', '')

    if q:
        subs = subs.filter(name__icontains=q)
    if category:
        subs = subs.filter(category=category)
    if billing:
        subs = subs.filter(billing_cycle=billing)
    if status == 'active':
        subs = subs.filter(is_active=True)
    elif status == 'inactive':
        subs = subs.filter(is_active=False)

    template = 'subscriptions/subscription_list.html'
    if request.headers.get('HX-Request'):
        template = 'subscriptions/subscription_list_partial.html'

    return render(request, template, {
        'subscriptions': subs.order_by('renewal_date'),
        'categories': Subscription.CATEGORY_CHOICES,
        'filters': request.GET,
    })


@login_required
def subscription_cancel(request, pk):
    """Abonelik iptal et."""
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == 'POST':
        sub.is_active = False
        sub.cancelled_at = timezone.now().date()
        sub.save()
        messages.success(request, f'"{sub.name}" aboneliği iptal edildi.')
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)
