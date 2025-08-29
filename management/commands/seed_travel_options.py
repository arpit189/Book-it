from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from bookings.models import TravelOption


class Command(BaseCommand):
    help = 'Seed the database with sample travel options'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample travel options...')

        # Clear existing travel options
        TravelOption.objects.all().delete()

        # Sample data
        travel_options = [
            # Flights
            {
                'type': 'flight',
                'title': 'AI-101 Flight',
                'source': 'New York',
                'destination': 'London',
                'departure_datetime': timezone.now() + timedelta(days=2),
                'price': Decimal('850.00'),
                'available_seats': 150,
            },
            {
                'type': 'flight',
                'title': 'BA-202 Flight',
                'source': 'London',
                'destination': 'Paris',
                'departure_datetime': timezone.now() + timedelta(days=1),
                'price': Decimal('320.00'),
                'available_seats': 120,
            },
            {
                'type': 'flight',
                'title': 'LH-303 Flight',
                'source': 'Berlin',
                'destination': 'Rome',
                'departure_datetime': timezone.now() + timedelta(days=3),
                'price': Decimal('450.00'),
                'available_seats': 80,
            },
            {
                'type': 'flight',
                'title': 'AF-404 Flight',
                'source': 'Paris',
                'destination': 'Tokyo',
                'departure_datetime': timezone.now() + timedelta(days=5),
                'price': Decimal('1200.00'),
                'available_seats': 200,
            },
            {
                'type': 'flight',
                'title': 'UA-505 Flight',
                'source': 'Chicago',
                'destination': 'Los Angeles',
                'departure_datetime': timezone.now() + timedelta(days=1),
                'price': Decimal('280.00'),
                'available_seats': 180,
            },
            
            # Trains
            {
                'type': 'train',
                'title': 'Eurostar Express',
                'source': 'London',
                'destination': 'Paris',
                'departure_datetime': timezone.now() + timedelta(days=2),
                'price': Decimal('120.00'),
                'available_seats': 300,
            },
            {
                'type': 'train',
                'title': 'ICE High Speed',
                'source': 'Berlin',
                'destination': 'Munich',
                'departure_datetime': timezone.now() + timedelta(days=1),
                'price': Decimal('85.00'),
                'available_seats': 250,
            },
            {
                'type': 'train',
                'title': 'TGV Express',
                'source': 'Paris',
                'destination': 'Lyon',
                'departure_datetime': timezone.now() + timedelta(days=3),
                'price': Decimal('65.00'),
                'available_seats': 200,
            },
            {
                'type': 'train',
                'title': 'Acela Express',
                'source': 'New York',
                'destination': 'Boston',
                'departure_datetime': timezone.now() + timedelta(days=1),
                'price': Decimal('95.00'),
                'available_seats': 150,
            },
            {
                'type': 'train',
                'title': 'Shinkansen Bullet',
                'source': 'Tokyo',
                'destination': 'Osaka',
                'departure_datetime': timezone.now() + timedelta(days=2),
                'price': Decimal('130.00'),
                'available_seats': 400,
            },
            
            # Buses
            {
                'type': 'bus',
                'title': 'Greyhound Express',
                'source': 'New York',
                'destination': 'Washington DC',
                'departure_datetime': timezone.now() + timedelta(days=1),
                'price': Decimal('45.00'),
                'available_seats': 50,
            },
            {
                'type': 'bus',
                'title': 'Megabus Premium',
                'source': 'London',
                'destination': 'Manchester',
                'departure_datetime': timezone.now() + timedelta(days=2),
                'price': Decimal('25.00'),
                'available_seats': 60,
            },
            {
                'type': 'bus',
                'title': 'FlixBus Comfort',
                'source': 'Berlin',
                'destination': 'Hamburg',
                'departure_datetime': timezone.now() + timedelta(days=1),
                'price': Decimal('35.00'),
                'available_seats': 45,
            },
            {
                'type': 'bus',
                'title': 'National Express',
                'source': 'Birmingham',
                'destination': 'Liverpool',
                'departure_datetime': timezone.now() + timedelta(days=3),
                'price': Decimal('20.00'),
                'available_seats': 40,
            },
            {
                'type': 'bus',
                'title': 'Coach USA',
                'source': 'Los Angeles',
                'destination': 'San Francisco',
                'departure_datetime': timezone.now() + timedelta(days=2),
                'price': Decimal('55.00'),
                'available_seats': 55,
            },
        ]

        # Create travel options
        created_options = []
        for option_data in travel_options:
            travel_option = TravelOption.objects.create(**option_data)
            created_options.append(travel_option)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(created_options)} travel options!'
            )
        )

        # Display summary
        flight_count = TravelOption.objects.filter(type='flight').count()
        train_count = TravelOption.objects.filter(type='train').count()
        bus_count = TravelOption.objects.filter(type='bus').count()

        self.stdout.write(f'Flights: {flight_count}')
        self.stdout.write(f'Trains: {train_count}')
        self.stdout.write(f'Buses: {bus_count}')
