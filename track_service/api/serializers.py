from rest_framework import serializers

from loads.models import Load, LoadTruck, Location, Truck


class TruckSerializer(serializers.ModelSerializer):
    """Serializer for update Truck."""
    location = serializers.SlugRelatedField(
        queryset=Location.objects.all(),
        slug_field='zip',
    )

    class Meta:
        model = Truck
        fields = ('id', 'uid', 'location', 'capacity')
        read_only_fields = ('uid', 'capacity')


class LoadBaseSerializer(serializers.ModelSerializer):
    """Base serializer for load."""
    pick_up = serializers.SlugRelatedField(
        queryset=Location.objects.all(),
        slug_field='zip',
    )
    delivery = serializers.SlugRelatedField(
        queryset=Location.objects.all(),
        slug_field='zip',
    )


class LoadCreateSerializer(LoadBaseSerializer):
    """Serializer for create view."""
    class Meta:
        model = Load
        fields = ('id', 'pick_up', 'delivery', 'weight', 'description')


class LoadUpdateSerializer(LoadBaseSerializer):
    """Serializer for update Loads.."""
    class Meta:
        model = Load
        fields = ('id', 'pick_up', 'delivery', 'weight', 'description')
        read_only_fields = ('weight', 'description')


class LoadListSerializer(LoadBaseSerializer):
    """Serializer for list view of Loads."""
    near_trucks = serializers.IntegerField()

    class Meta:
        model = Load
        fields = ('id', 'pick_up', 'delivery', 'near_trucks')


class TruckDistanceSerializer(serializers.ModelSerializer):
    """Serializer for truck - distance."""
    truck = serializers.SlugRelatedField(
        slug_field='uid',
        read_only=True
    )

    class Meta:
        fields = ('truck', 'distance')
        model = LoadTruck


class LoadRetrieveSerializer(LoadBaseSerializer):
    """Serializer for retrieve Load."""
    trucks = TruckDistanceSerializer(many=True)

    class Meta:
        model = Load
        fields = (
            'id', 'pick_up', 'delivery', 'weight', 'description', 'trucks'
        )
