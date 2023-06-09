import random
import string

from geopy.distance import distance
from django.conf import settings
from django.core.management.base import BaseCommand

from loads import models


_LETTERS = string.ascii_uppercase
TRUCKS = settings.TRUCKS
UID_START_INDEX = settings.UID_START_INDEX
MIN_WEIGHT = settings.MIN_WEIGHT
MAX_WEIGHT = settings.MAX_WEIGHT


def _generate_uid(index):
    """Generate uid."""
    rand_letter = random.choice(_LETTERS)
    return str(UID_START_INDEX + index) + rand_letter


def _create_load_truck(trucks):
    """Create relations between load and truck if needed."""
    loads = models.Load.objects.select_related('pick_up').all()
    if loads.exists():
        load_truck = []
        for truck in trucks:
            truck_loc = (truck.location.latitude, truck.location.longitude)
            for load in loads:
                load_loc = (load.pick_up.latitude, load.pick_up.longitude)
                obj = models.LoadTruck(
                    load=load,
                    truck=truck,
                    distance=round(distance(load_loc, truck_loc).miles, 2)
                )
                load_truck.append(obj)
        models.LoadTruck.objects.bulk_create(load_truck)


class Command(BaseCommand):
    help = "Create several random trucks."

    def handle(self, *args, **options):
        _LOCATIONS = models.Location.objects.last().id
        model = models.Truck
        object_model = model.objects.all()
        object_model.delete()
        trucks = [model(
                uid=_generate_uid(i),
                location_id=random.randint(1, _LOCATIONS),
                capacity=random.randint(MIN_WEIGHT, MAX_WEIGHT),
            ) for i in range(TRUCKS)
        ]
        created_objects = model.objects.bulk_create(trucks)

        _create_load_truck(trucks)

        created_count = len(created_objects)
        self.stdout.write(
            self.style.SUCCESS(
                f'({model}) Создано записей: {created_count}'
            )
        )
