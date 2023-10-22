from django_filters import FilterSet, CharFilter, ChoiceFilter, DateFromToRangeFilter, BooleanFilter
from django_filters.widgets import RangeWidget, BooleanWidget
from MessageBoard.models import CATEGORIES

######################################################################################################################


class AdvFilter(FilterSet):
    category = ChoiceFilter(
        label='Категория:',
        choices=CATEGORIES,
    )
    title = CharFilter(
        label='Заголовок:',
        field_name='title',
        lookup_expr='icontains',
    )
    author = CharFilter(
        label="Автор:",
        field_name='author__username',
        lookup_expr='icontains',
    )
    date_of_creation = DateFromToRangeFilter(
        label='Диапазон дат:',
        field_name='create_date',
        widget=RangeWidget(
            attrs={'type': 'date'},
        ),
    )


######################################################################################################################


class ProfileAdvFilter(FilterSet):
    category = ChoiceFilter(
        label='Категория:',
        choices=CATEGORIES,
    )
    title = CharFilter(
        label='Заголовок:',
        field_name='title',
        lookup_expr='icontains',
    )
    date = DateFromToRangeFilter(
        label='Диапазон дат:',
        field_name='create_date',
        widget=RangeWidget(
            attrs={'type': 'date'},
        ),
    )


######################################################################################################################


class ProfileReplyFilter(FilterSet):
    date = DateFromToRangeFilter(
        label='Диапазон дат:',
        field_name='create_date',
        widget=RangeWidget(
            attrs={'type': 'date'},
        ),
    )
    approved = BooleanFilter(
        label='Approved?',
        field_name='is_approved',
        widget=BooleanWidget(),
    )
    rejected = BooleanFilter(
        label='Rejected?',
        field_name='is_rejected',
        widget=BooleanWidget(),
    )


######################################################################################################################
