from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from . import utils
from .validators import validate_zip_code

MIN_WEIGHT = 1
MAX_WEIGHT = 1000


class Location(models.Model):
    """Locations."""
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    zip = models.CharField(
        max_length=128,
        unique=True,
        validators=[validate_zip_code]
    )
    latitude = models.FloatField()
    longitude = models.FloatField()


class LoadTruck(models.Model):
    """M-M Relations of loads and truck."""
    load = models.ForeignKey(
        'Load',
        on_delete=models.CASCADE,
        related_name='trucks',
    )
    truck = models.ForeignKey(
        'Truck',
        on_delete=models.CASCADE,
        related_name='loads',
    )
    distance = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['load', 'truck'],
                name='unique_load_truck'
            )
        ]


class Load(models.Model):
    """Loads."""
    pick_up = models.ForeignKey(
        'Location',
        on_delete=models.CASCADE,
        related_name='load',
    )
    delivery = models.ForeignKey(
        'Location',
        on_delete=models.CASCADE,
        related_name='destination',
    )
    weight = models.SmallIntegerField(
        validators=[
            MaxValueValidator(MAX_WEIGHT),
            MinValueValidator(MIN_WEIGHT)
        ]
    )
    description = models.CharField()
    truck = models.ManyToManyField(
        'Truck', related_name='load', through="LoadTruck"
    )

    class Meta:
        ordering = ('-id',)

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        new_obj = False
        if self._is_new_object():
            new_obj = True
        super().save(force_insert, force_update, *args, **kwargs)
        if new_obj:
            utils.create_load_trucks(load=self)

    def _is_new_object(self):
        return self.pk is None


class Truck(models.Model):
    """Trucks."""
    uid = models.CharField(max_length=16, unique=True)
    location = models.ForeignKey(
        'location',
        on_delete=utils.set_location,
        related_name='truck',
        default=utils.set_location,
    )
    capacity = models.SmallIntegerField(
        validators=[
            MaxValueValidator(MAX_WEIGHT),
            MinValueValidator(MIN_WEIGHT)
        ]
    )

    __location = None

    class Meta:
        ordering = ('-id',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__location = self.location

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        new_obj = False
        if self._is_location_changed() and self._is_new_object():
            new_obj = True
        else:
            utils.update_distances_for_loads(self)
        super().save(force_insert, force_update, *args, **kwargs)
        if new_obj:
            utils.create_load_trucks(truck=self)
        self._update_location()

    def _is_location_changed(self):
        return self.location != self.__location

    def _update_location(self):
        self.__location = self.location

    def _is_new_object(self):
        return self.pk is None
