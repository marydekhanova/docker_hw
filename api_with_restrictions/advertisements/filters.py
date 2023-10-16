from django_filters.rest_framework import DateFromToRangeFilter, \
    FilterSet, DateFilter

from advertisements.models import Advertisement


class AdvertisementFilter(FilterSet):
    date = DateFilter(field_name='created_at__date')
    date_range = DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Advertisement
        fields = ['status', 'date', 'date_range']
