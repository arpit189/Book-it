from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile, TravelOption, Booking


class UserRegistrationForm(UserCreationForm):
    """Custom user registration form with email."""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email address is already in use.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create user profile
            UserProfile.objects.create(user=user)
        return user


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile."""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ('phone', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Update user fields
            profile.user.first_name = self.cleaned_data['first_name']
            profile.user.last_name = self.cleaned_data['last_name']
            profile.user.email = self.cleaned_data['email']
            profile.user.save()
            profile.save()
        return profile


class BookingForm(forms.ModelForm):
    """Form for creating bookings."""
    num_seats = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    )

    class Meta:
        model = Booking
        fields = ('num_seats',)

    def __init__(self, *args, **kwargs):
        self.travel_option = kwargs.pop('travel_option', None)
        super().__init__(*args, **kwargs)
        if self.travel_option:
            self.fields['num_seats'].max_value = self.travel_option.available_seats
            self.fields['num_seats'].widget.attrs['max'] = self.travel_option.available_seats

    def clean_num_seats(self):
        num_seats = self.cleaned_data.get('num_seats')
        if self.travel_option and num_seats > self.travel_option.available_seats:
            raise ValidationError(
                f'Only {self.travel_option.available_seats} seats are available.'
            )
        return num_seats


class TravelSearchForm(forms.Form):
    """Form for searching travel options."""
    TRAVEL_TYPES = [('', 'All Types')] + TravelOption.TRAVEL_TYPES

    type = forms.ChoiceField(
        choices=TRAVEL_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    source = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'From'})
    )
    destination = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'To'})
    )
    departure_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    min_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min Price'})
    )
    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max Price'})
    )

    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')
        
        if min_price and max_price and min_price > max_price:
            raise ValidationError('Minimum price cannot be greater than maximum price.')
        
        return cleaned_data
