from rest_framework import viewsets
from rest_framework import generics
from django.db.models import Count, Case, When

from . import serializers
from loads.models import Truck, Load

LOAD_SERIALIZERS = {
    'list': serializers.LoadListSerializer,
    'update': serializers.LoadUpdateSerializer,
    'partial_update': serializers.LoadUpdateSerializer,
    'create': serializers.LoadCreateSerializer,
    'retrieve': serializers.LoadRetrieveSerializer
}


class TruckUpdateView(generics.UpdateAPIView):
    """View for update truck."""
    queryset = Truck.objects.all()
    serializer_class = serializers.TruckSerializer


class LoadViewSet(viewsets.ModelViewSet):
    """View set for Loads."""
    queryset = Load.objects.all()

    def get_serializer_class(self):
        return LOAD_SERIALIZERS.get(
            self.action, serializers.LoadRetrieveSerializer)

    def get_queryset(self):
        if self.action == 'list':
            return Load.objects.all().annotate(
                near_trucks=Count(Case(When(
                    trucks__distance__lte=450,
                    then=1
                )))
            )
        return Load.objects.all()
