from django.db import models
from django.contrib.auth.models import User

class MeterReading(models.Model):
    UTILITY_CHOICES = [
        ('Energy', 'Energy'),
        ('Hot Water', 'Hot Water'),
        ('Heating', 'Heating'),
        ('Cold Water', 'Cold Water'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    utility_type = models.CharField(max_length=20, choices=UTILITY_CHOICES)
    reading_value = models.DecimalField(max_digits=10, decimal_places=3)
    
    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'date', 'utility_type'],
                name='unique_reading_per_user_month_utility',
                violation_error_message='A reading for this user, month and utility already exists.',
            )
        ]

    def save(self, *args, **kwargs):
        # Readings are monthly - always store them on the 1st day of the month
        if self.date:
            self.date = self.date.replace(day=1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.utility_type} - {self.date}: {self.reading_value}"


class FeeRate(models.Model):
    FEE_TYPES = [
        ('heating', 'Heating Energy (CO)'),
        ('hot_water', 'Hot Water Energy (CWU)'),
        ('cold_water', 'Cold Water'),
    ]
    year = models.PositiveIntegerField(verbose_name="Year")
    fee_type = models.CharField(max_length=20, choices=FEE_TYPES, verbose_name="Fee Type")
    quantity_included = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Quantity included in rent")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Price")

    class Meta:
        ordering = ['-year', 'fee_type']
        constraints = [
            models.UniqueConstraint(fields=['year', 'fee_type'], name='unique_fee_rate_per_year')
        ]

    def __str__(self):
        return f"{self.year} - {self.get_fee_type_display()}"

