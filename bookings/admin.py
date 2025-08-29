from django.contrib import admin
from .models import TravelOption, Booking, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('created_at',)


@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'source', 'destination', 'departure_datetime', 'price', 'available_seats', 'created_at')
    list_filter = ('type', 'source', 'destination', 'departure_datetime', 'created_at')
    search_fields = ('title', 'source', 'destination')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('departure_datetime',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('type', 'title', 'source', 'destination')
        }),
        ('Schedule & Pricing', {
            'fields': ('departure_datetime', 'price', 'available_seats')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'travel_option', 'num_seats', 'total_price', 'status', 'booking_date')
    list_filter = ('status', 'booking_date', 'travel_option__type')
    search_fields = ('user__username', 'user__email', 'travel_option__title')
    readonly_fields = ('booking_date', 'updated_at')
    ordering = ('-booking_date',)
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('user', 'travel_option', 'num_seats', 'total_price', 'status')
        }),
        ('Timestamps', {
            'fields': ('booking_date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'travel_option')
