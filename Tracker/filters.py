import django_filters
from .models import *
from django import forms
from django_filters import DateFilter, CharFilter

class ProfileFilter(django_filters.FilterSet):
    RollNo= CharFilter(field_name='RollNo', lookup_expr='icontains')
    Branch= CharFilter(field_name='Branch', lookup_expr='icontains')
    Company= CharFilter(field_name='Company', lookup_expr='icontains')
    class Meta:
        model=Profile
        fields=['RollNo','Year','Branch','Company']
        exclude=['Image']