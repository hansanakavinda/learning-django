import django_filters
from .models import Job

class JobFilter(django_filters.FilterSet):
    # Exact match
    job_type = django_filters.CharFilter(lookup_expr='exact')

    # Range filters for salary
    salary_min = django_filters.NumberFilter(
        field_name='salary_min',
        lookup_expr='gte'    # greater than or equal
    )
    salary_max = django_filters.NumberFilter(
        field_name='salary_max',
        lookup_expr='lte'    # less than or equal
    )

    # Filter by company name (case insensitive contains)
    company = django_filters.CharFilter(
        field_name='company__name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Job
        fields = ['job_type', 'is_active', 'company']