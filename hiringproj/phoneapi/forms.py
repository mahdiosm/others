from django import forms
from django.core.exceptions import ValidationError
from .models import Phone


def validate_price(value):
    if not isinstance(value, int) or value <= 0:
        raise ValidationError("قیمت باید عددی بزرگتر از 0 باشد.")


def validate_screen_size(value):
    if value <= 0:
        raise ValidationError("اندازه صفحه باید عددی بزرگتر از 0 باشد.")


class PhoneSearchForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'جستجو...'
        })
    )
    brands = forms.MultipleChoiceField(
        choices=[(brand, brand) for brand in Phone.objects.values_list('brand', flat=True).distinct()],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="انتخاب برند"
    )

    brand_country = forms.MultipleChoiceField(
        choices=[(country, country) for country in Phone.objects.values_list('brand_country', flat=True).distinct()],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="انتخاب کشور برند"
    )

    match_countries = forms.BooleanField(
        required=False,
        label="تطابق کشور سازنده و کشور برند"
    )

    is_available = forms.BooleanField(
        required=False,
        label="فقط موجود‌ها",
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['brand', 'brand_country', 'model', 'price', 'color', 'screen_size', 'is_available', 'creator_country']
        labels = {
            'brand': 'نام برند',
            'brand_country': 'کشور برند',
            'model': 'مدل',
            'price': 'قیمت',
            'color': 'رنگ',
            'screen_size': 'اندازه صفحه',
            'is_available': 'موجودی',
            'creator_country': 'کشور سازنده',
        }

        error_messages = {
            'model': {
                'unique': "مدل باید یکتا باشد.",
            },
        }

        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_country': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'screen_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.Select(attrs={'class': 'form-control'}),
            'creator_country': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        validate_price(price)
        return price

    def clean_screen_size(self):
        screen_size = self.cleaned_data.get('screen_size')
        validate_screen_size(screen_size)
        return screen_size
