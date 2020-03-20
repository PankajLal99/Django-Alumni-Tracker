import django_filters
from .models import *
from django import forms
from django_filters import DateFilter, CharFilter

class ProfileFilter(django_filters.FilterSet):
    Branch= CharFilter(field_name='Branch', lookup_expr='icontains')
    Company= CharFilter(field_name='Company', lookup_expr='icontains')
    class Meta:
        model=Profile
        fields=['RollNo','Year','Branch','Company']
        #fields='__all__'
        exclude=['Image']
      
        