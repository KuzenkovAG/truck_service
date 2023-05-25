import random

from geopy.distance import distance

from . import models


def set_location():
    """Set random location."""
    return random.choice(list(models.Location.objects.all()))


def create_load_trucks(load=None, truck=None):
    """Create relations between load and trucks, depend on load or truck."""
    if load:
        trucks = models.Truck.objects.select_related('location').all()
        load_loc = (load.pick_up.latitude, load.pick_up.longitude)
        obj = [models.LoadTruck(
                load=load,
                truck=truck,
                distance=round(distance(load_loc, (
                    truck.location.latitude, truck.location.longitude
                )).miles, 2)
            ) for truck in trucks
        ]
    else:
        loads = models.Load.objects.select_related('pick_up').all()
        truck_loc = (truck.location.latitude, load.location.longitude)
        obj = [models.LoadTruck(
                load=load,
                truck=truck,
                distance=round(distance(truck_loc, (
                    load.pick_up.latitude, load.pick_up.longitude
                )).miles, 2)
            ) for load in loads
        ]
    models.LoadTruck.objects.bulk_create(obj)


def update_distances_for_loads(truck):
    """Update distances between load and trucks if changed truck location."""
    loc1 = (truck.location.latitude, truck.location.longitude)
    loads = truck.loads.select_related('load__pick_up')
    for load in loads:
        loc2 = (
            load.load.pick_up.latitude,
            load.load.pick_up.longitude
        )
        load.distance = round(distance(loc1, loc2).miles, 2)
    models.LoadTruck.objects.bulk_update(loads, ['distance'])
