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


class LoadUpdateSerializer(serializers.ModelSerializer):
    """Serializer for update Load."""
    pick_up = serializers.SlugRelatedField(
        read_only=True,
        slug_field='zip',
    )
    delivery = serializers.SlugRelatedField(
        read_only=True,
        slug_field='zip',
    )

    class Meta:
        model = Load
        fields = ('id', 'pick_up', 'delivery', 'weight', 'description')


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
    """Serializer for create Load."""
    class Meta:
        model = Load
        fields = ('id', 'pick_up', 'delivery', 'weight', 'description')


class LoadListSerializer(LoadBaseSerializer):
    """Serializer for list view of Load."""
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
