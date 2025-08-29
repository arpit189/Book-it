from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.db import transaction

from .models import TravelOption, Booking, UserProfile
from .forms import UserRegistrationForm, UserProfileForm, BookingForm, TravelSearchForm


def home(request):
    """Home page with search form and featured travel options."""
    search_form = TravelSearchForm(request.GET or None)
    travel_options = TravelOption.objects.filter(
        departure_datetime__gte=timezone.now()
    ).order_by('departure_datetime')[:6]

    context = {
        'search_form': search_form,
        'travel_options': travel_options,
    }
    return render(request, 'home.html', context)


def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Travel Booker.')
            return redirect('bookings:home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    """User profile view."""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('bookings:profile')
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'registration/profile.html', context)


def travel_list(request):
    """List all travel options with filtering and pagination."""
    search_form = TravelSearchForm(request.GET or None)
    travel_options = TravelOption.objects.filter(
        departure_datetime__gte=timezone.now()
    ).order_by('departure_datetime')

    # Apply filters
    if search_form.is_valid():
        if search_form.cleaned_data.get('type'):
            travel_options = travel_options.filter(
                type=search_form.cleaned_data['type']
            )
        if search_form.cleaned_data.get('source'):
            travel_options = travel_options.filter(
                source__icontains=search_form.cleaned_data['source']
            )
        if search_form.cleaned_data.get('destination'):
            travel_options = travel_options.filter(
                destination__icontains=search_form.cleaned_data['destination']
            )
        if search_form.cleaned_data.get('departure_date'):
            travel_options = travel_options.filter(
                departure_datetime__date=search_form.cleaned_data['departure_date']
            )
        if search_form.cleaned_data.get('min_price'):
            travel_options = travel_options.filter(
                price__gte=search_form.cleaned_data['min_price']
            )
        if search_form.cleaned_data.get('max_price'):
            travel_options = travel_options.filter(
                price__lte=search_form.cleaned_data['max_price']
            )

    # Pagination
    paginator = Paginator(travel_options, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'search_form': search_form,
        'page_obj': page_obj,
        'travel_options': page_obj,
    }
    return render(request, 'bookings/travel_list.html', context)


def travel_detail(request, pk):
    """Travel option detail view with booking form."""
    travel_option = get_object_or_404(TravelOption, pk=pk)
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = BookingForm(request.POST, travel_option=travel_option)
        if form.is_valid():
            try:
                with transaction.atomic():
                    booking = form.save(commit=False)
                    booking.user = request.user
                    booking.travel_option = travel_option
                    booking.save()
                    messages.success(
                        request, 
                        f'Booking confirmed! You have booked {booking.num_seats} seat(s) for {travel_option.title}.'
                    )
                    return redirect('bookings:booking_detail', pk=booking.pk)
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = BookingForm(travel_option=travel_option)

    context = {
        'travel_option': travel_option,
        'form': form,
    }
    return render(request, 'bookings/travel_detail.html', context)


@login_required
def booking_list(request):
    """List user's bookings with filtering."""
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    # Pagination
    paginator = Paginator(bookings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'bookings': page_obj,
        'status_filter': status_filter,
    }
    return render(request, 'bookings/booking_list.html', context)


@login_required
def booking_detail(request, pk):
    """Booking detail view."""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/booking_detail.html', context)


@login_required
@require_POST
def cancel_booking(request, pk):
    """Cancel a booking."""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    if booking.can_cancel:
        if booking.cancel():
            messages.success(request, 'Booking cancelled successfully!')
        else:
            messages.error(request, 'Failed to cancel booking.')
    else:
        messages.error(request, 'This booking cannot be cancelled.')
    
    return redirect('bookings:booking_list')


def search_autocomplete(request):
    """AJAX endpoint for search autocomplete."""
    query = request.GET.get('q', '')
    field = request.GET.get('field', '')
    
    if not query or len(query) < 2:
        return JsonResponse({'results': []})
    
    if field == 'source':
        results = TravelOption.objects.filter(
            source__icontains=query
        ).values_list('source', flat=True).distinct()[:10]
    elif field == 'destination':
        results = TravelOption.objects.filter(
            destination__icontains=query
        ).values_list('destination', flat=True).distinct()[:10]
    else:
        results = []
    
    return JsonResponse({'results': list(results)})
