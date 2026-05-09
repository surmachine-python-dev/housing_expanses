from django import forms
from .models import MeterReading, FeeRate

class MeterReadingForm(forms.ModelForm):
    class Meta:
        model = MeterReading
        fields = ['user', 'date', 'utility_type', 'reading_value']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({'class': 'form-select'})
        self.fields['date'].widget.attrs.update({'class': 'form-control'})
        self.fields['utility_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['reading_value'].widget.attrs.update({'class': 'form-control', 'step': '0.01'})

class FeeRateForm(forms.ModelForm):
    class Meta:
        model = FeeRate
        fields = ['year', 'fee_type', 'quantity_included', 'unit_price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year'].widget.attrs.update({'class': 'form-control'})
        self.fields['fee_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['quantity_included'].widget.attrs.update({'class': 'form-control', 'step': '0.01'})
        self.fields['unit_price'].widget.attrs.update({'class': 'form-control', 'step': '0.01'})

