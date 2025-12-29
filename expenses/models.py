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

    def __str__(self):
        return f"{self.user.username} - {self.utility_type} - {self.date}: {self.reading_value}"

