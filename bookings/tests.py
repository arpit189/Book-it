from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta

from .models import TravelOption, Booking, UserProfile


class UserRegistrationTest(TestCase):
    """Test user registration functionality."""
    
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('bookings:register')
        
    def test_user_registration_success(self):
        """Test successful user registration."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(hasattr(user, 'profile'))


class TravelOptionModelTest(TestCase):
    """Test TravelOption model functionality."""
    
    def setUp(self):
        self.travel_option = TravelOption.objects.create(
            type='flight',
            title='Test Flight',
            source='New York',
            destination='London',
            departure_datetime=timezone.now() + timedelta(days=1),
            price=Decimal('500.00'),
            available_seats=100
        )
        
    def test_travel_option_creation(self):
        """Test travel option creation."""
        self.assertEqual(self.travel_option.title, 'Test Flight')
        self.assertEqual(self.travel_option.available_seats, 100)
        
    def test_is_available(self):
        """Test seat availability check."""
        self.assertTrue(self.travel_option.is_available(50))
        self.assertFalse(self.travel_option.is_available(150))


class BookingModelTest(TestCase):
    """Test Booking model functionality."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.travel_option = TravelOption.objects.create(
            type='flight',
            title='Test Flight',
            source='New York',
            destination='London',
            departure_datetime=timezone.now() + timedelta(days=1),
            price=Decimal('500.00'),
            available_seats=100
        )
        
    def test_booking_creation_success(self):
        """Test successful booking creation."""
        initial_seats = self.travel_option.available_seats
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            num_seats=5
        )
        
        self.assertEqual(booking.num_seats, 5)
        self.assertEqual(booking.total_price, Decimal('2500.00'))
        
        self.travel_option.refresh_from_db()
        self.assertEqual(self.travel_option.available_seats, initial_seats - 5)
        
    def test_booking_cancellation_success(self):
        """Test successful booking cancellation."""
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            num_seats=10
        )
        initial_seats = self.travel_option.available_seats
        
        success = booking.cancel()
        
        self.assertTrue(success)
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')
        
        self.travel_option.refresh_from_db()
        self.assertEqual(self.travel_option.available_seats, initial_seats + 10)


class BookingViewsTest(TestCase):
    """Test booking views functionality."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.travel_option = TravelOption.objects.create(
            type='flight',
            title='Test Flight',
            source='New York',
            destination='London',
            departure_datetime=timezone.now() + timedelta(days=1),
            price=Decimal('500.00'),
            available_seats=100
        )
        
    def test_home_page(self):
        """Test home page loads correctly."""
        response = self.client.get(reverse('bookings:home'))
        self.assertEqual(response.status_code, 200)
        
    def test_booking_creation_authenticated(self):
        """Test booking creation by authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('bookings:travel_detail', args=[self.travel_option.pk]),
            {'num_seats': 5}
        )
        
        self.assertEqual(response.status_code, 302)
        booking = Booking.objects.get(user=self.user, travel_option=self.travel_option)
        self.assertEqual(booking.num_seats, 5)
        
    def test_booking_list_unauthenticated(self):
        """Test booking list redirect for unauthenticated user."""
        response = self.client.get(reverse('bookings:booking_list'))
        self.assertEqual(response.status_code, 302)


class PermissionTest(TestCase):
    """Test permission and security."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.travel_option = TravelOption.objects.create(
            type='flight',
            title='Test Flight',
            source='New York',
            destination='London',
            departure_datetime=timezone.now() + timedelta(days=1),
            price=Decimal('500.00'),
            available_seats=100
        )
        
    def test_user_cannot_access_others_booking_detail(self):
        """Test user cannot access another user's booking detail."""
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            num_seats=5
        )
        
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(
            reverse('bookings:booking_detail', args=[booking.pk])
        )
        
        self.assertEqual(response.status_code, 404)
