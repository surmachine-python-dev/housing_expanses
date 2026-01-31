from django import forms
from .models import MeterReading, FeeRate

class MeterReadingForm(forms.ModelForm):
    class Meta:
        model = MeterReading
        fields = ['user', 'date', 'utility_type', 'reading_value']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class FeeRateForm(forms.ModelForm):
    class Meta:
        model = FeeRate
        fields = ['year', 'fee_type', 'quantity_included', 'unit_price']

