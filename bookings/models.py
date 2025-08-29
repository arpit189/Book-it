from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import transaction
from decimal import Decimal


class UserProfile(models.Model):
    """Extended user profile with additional fields."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class TravelOption(models.Model):
    """Model for travel options (flights, trains, buses)."""
    TRAVEL_TYPES = [
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
    ]

    type = models.CharField(max_length=10, choices=TRAVEL_TYPES)
    title = models.CharField(max_length=200)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_datetime = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    available_seats = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['departure_datetime']
        indexes = [
            models.Index(fields=['type', 'source', 'destination']),
            models.Index(fields=['departure_datetime']),
        ]

    def __str__(self):
        return f"{self.title} - {self.source} to {self.destination}"

    def is_available(self, num_seats=1):
        """Check if requested number of seats are available."""
        return self.available_seats >= num_seats

    def book_seats(self, num_seats):
        """Atomically book seats and return success status."""
        with transaction.atomic():
            # Use select_for_update to prevent race conditions
            travel_option = TravelOption.objects.select_for_update().get(id=self.id)
            if travel_option.available_seats >= num_seats:
                travel_option.available_seats -= num_seats
                travel_option.save()
                return True
            return False


class Booking(models.Model):
    """Model for user bookings."""
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE, related_name='bookings')
    num_seats = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    booking_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-booking_date']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['travel_option', 'status']),
        ]

    def __str__(self):
        return f"Booking {self.id} - {self.user.username} - {self.travel_option.title}"

    def save(self, *args, **kwargs):
        """Override save to calculate total price and handle seat booking."""
        if not self.pk:  # New booking
            self.total_price = self.travel_option.price * self.num_seats
            # Book seats atomically
            if not self.travel_option.book_seats(self.num_seats):
                raise ValueError(f"Not enough seats available. Requested: {self.num_seats}, Available: {self.travel_option.available_seats}")
        super().save(*args, **kwargs)

    def cancel(self):
        """Cancel booking and restore seats."""
        if self.status == 'confirmed':
            with transaction.atomic():
                # Use select_for_update to prevent race conditions
                travel_option = TravelOption.objects.select_for_update().get(id=self.travel_option.id)
                travel_option.available_seats += self.num_seats
                travel_option.save()
                
                self.status = 'cancelled'
                self.save()
                return True
        return False

    @property
    def can_cancel(self):
        """Check if booking can be cancelled."""
        return self.status == 'confirmed'
