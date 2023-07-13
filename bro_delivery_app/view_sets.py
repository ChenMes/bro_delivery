from rest_framework import mixins

import django_filters
from django_filters import FilterSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from bro_delivery_app.models import Delivery
from bro_delivery_app.serializers import DeliverySerializer


class DeliveryFilterSet(FilterSet):
    preparation_time = django_filters.CharFilter(field_name='preparation_time', lookup_expr='iexact')
    arrival_time = django_filters.NumberFilter('duration_in_min', lookup_expr='gte')
    time_left = django_filters.NumberFilter('duration_in_min', lookup_expr='lte')
    payment = django_filters.BooleanFilter(default=False)
    price = django_filters.NumberFilter('duration_in_min', lookup_expr='gte')
    address = django_filters.CharFilter(field_name='address', lookup_expr='iexact')
    restaurant = django_filters.CharFilter(field_name='restaurant', lookup_expr='iexact')
    delivery_guys = None
    customer = None

    class Meta:
        model = Delivery
        fields = ['release_year']


class DeliveryPageClass(PageNumberPagination):
    page_size = 5


class DeliveryPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or view.action \
            in ('list', 'retrieve')

    def has_object_permission(self, request, view, obj):
        return view.action == 'retrieve' or \
            obj.created_by == request.user


class DeliveryViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all
    # pagination_class = DeliveryPageClass
    # filterset_class = DeliveryFilterSet
    # permission_classes = [DeliveryPermission]
