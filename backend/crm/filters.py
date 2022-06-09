import django_filters
from . import models


class LeadFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='contains',
        label='Название сделки'
    )
    budget__gte = django_filters.NumberFilter(
        field_name='budget',
        lookup_expr='gte',
        label='Бюджет от'
    )
    budget__lte = django_filters.NumberFilter(
        field_name='budget',
        lookup_expr='lte',
        label='Бюджет до'
    )
    stage = django_filters.ModelMultipleChoiceFilter(
        field_name='stage',
        label='Этап сделки',
        queryset=models.LeadStage.objects.all()
    )
    client_name = django_filters.CharFilter(
        field_name='client__name',
        label='Имя клиента',
        lookup_expr='contains'
    )
    client_phone_number = django_filters.CharFilter(
        field_name='client__phone_number',
        label='Номер телефона',
        lookup_expr='contains'
    )
    modified_at__gte = django_filters.NumberFilter(
        field_name='modified_at',
        lookup_expr='gte',
        label='Последнее изменение от'
    )
    modified_at__lte = django_filters.NumberFilter(
        field_name='modified_at',
        lookup_expr='lte',
        label='Последнее изменение до'
    )
    created_at__gte = django_filters.NumberFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Дата создания от'
    )
    created_at__lte = django_filters.NumberFilter(
        field_name='created_at',
        lookup_expr='lte',
        label='Дата создания до'
    )

    class Meta:
        model = models.Lead
