from django import forms
from .models import Subscription, CreditCard


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'price', 'billing_cycle', 'renewal_date',
                  'credit_card', 'category', 'is_active', 'cancelled_at', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Örn: Spotify Premium',
                'autocomplete': 'off',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
            }),
            'billing_cycle': forms.Select(attrs={
                'class': 'form-select',
            }),
            'renewal_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
            }),
            'credit_card': forms.Select(attrs={
                'class': 'form-select',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
            }),
            'cancelled_at': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Opsiyonel notlar...',
                'rows': 3,
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['credit_card'].queryset = CreditCard.objects.filter(user=user)


class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ['card_name', 'last_four', 'card_color']
        widgets = {
            'card_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Örn: Ziraat Bankası Visa',
            }),
            'last_four': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '1234',
                'maxlength': '4',
                'pattern': '[0-9]{4}',
            }),
            'card_color': forms.TextInput(attrs={
                'class': 'form-input',
                'type': 'color',
            }),
        }
