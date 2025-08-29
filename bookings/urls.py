from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # Home and search
    path('', views.home, name='home'),
    path('travel/', views.travel_list, name='travel_list'),
    path('travel/<int:pk>/', views.travel_detail, name='travel_detail'),
    path('search/autocomplete/', views.search_autocomplete, name='search_autocomplete'),
    
    # User management
    path('accounts/register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    
    # Bookings
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
]
