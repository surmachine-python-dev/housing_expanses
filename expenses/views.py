from django.shortcuts import render
from .models import MeterReading
from django.db.models import F
import json
from django.core.serializers.json import DjangoJSONEncoder

def dashboard(request):
    # For demonstration, fetch all readings. 
    # In a real app, you might filter by request.user
    readings = MeterReading.objects.all().order_by('date')
    
    # Prepare data for Chart.js
    # We want a line for each Utility Type (and maybe User?)
    # Let's group by Utility Type for simplicity first.
    
    # Get unique dates
    dates = sorted(list(set(readings.values_list('date', flat=True))))
    formatted_dates = [d.strftime('%Y-%m-%d') for d in dates]
    
    datasets = []
    
    # Get unique utilities
    utilities = MeterReading.UTILITY_CHOICES
    
    # distinct users
    users = set(readings.values_list('user__username', flat=True))

    # Let's create a dataset for each User-Utility combination
    colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
    color_index = 0

    for username in users:
        for util_code, util_name in utilities:
            # Filter readings for this user and utility
            user_readings = readings.filter(user__username=username, utility_type=util_code)
            if not user_readings.exists():
                continue
                
            data_points = []
            for d in dates:
                # Find reading for this date
                reading = user_readings.filter(date=d).first()
                if reading:
                    data_points.append(float(reading.reading_value))
                else:
                    data_points.append(None) # Gap in data
            
            datasets.append({
                'label': f'{username} - {util_name}',
                'data': data_points,
                'borderColor': colors[color_index % len(colors)],
                'fill': False,
                'spanGaps': True
            })
            color_index += 1

    context = {
        'readings': readings,
        'chart_labels': json.dumps(formatted_dates, cls=DjangoJSONEncoder),
        'chart_datasets': json.dumps(datasets, cls=DjangoJSONEncoder),
    }
    return render(request, 'expenses/dashboard.html', context)

