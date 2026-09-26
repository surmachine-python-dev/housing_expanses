from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import MeterReading, FeeRate
from .forms import MeterReadingForm, FeeRateForm

def dashboard(request):
    active_tab = request.GET.get('tab', 'Charts')

    if request.method == 'POST':
        if 'reading_submit' in request.POST:
            form = MeterReadingForm(request.POST)
            fee_form = FeeRateForm()
            if form.is_valid():
                form.save()
                messages.success(request, 'Saved successfully!')
                return redirect(f"{reverse('dashboard')}?tab=AddEntry")
            messages.error(request, 'Reading was not saved. Please correct the errors below.')
            active_tab = 'AddEntry'
        elif 'fee_submit' in request.POST:
            form = MeterReadingForm()
            fee_form = FeeRateForm(request.POST)
            if fee_form.is_valid():
                fee_form.save()
                messages.success(request, 'Fee rate saved successfully!')
                return redirect(f"{reverse('dashboard')}?tab=Fees")
            messages.error(request, 'Fee rate was not saved. Please correct the errors below.')
            active_tab = 'Fees'
        else:
            form = MeterReadingForm()
            fee_form = FeeRateForm()
    else:
        form = MeterReadingForm()
        fee_form = FeeRateForm()

    # For demonstration, fetch all readings. 
    # In a real app, you might filter by request.user
    readings = MeterReading.objects.all().order_by('date')
    
    # Readings for the table (descending order)
    readings_table = MeterReading.objects.all().order_by('-date')
    
    # Prepare data for Chart.js
    # We want a line for each Utility Type (and maybe User?)
    # Let's group by Utility Type for simplicity first.
    
    # Get unique dates
    dates = sorted(list(set(readings.values_list('date', flat=True))))
    # Format dates as "Month Year" (e.g., "January 2025")
    formatted_dates = [d.strftime('%B %Y') for d in dates]
    
    datasets_water = []

    datasets_energy = []
    datasets_heating = []
    
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
            user_readings = readings.filter(user__username=username, utility_type=util_code).order_by('date')
            if not user_readings.exists():
                continue
                
            data_points = []
            
            # Pre-fetch readings into a dictionary for easier lookup
            readings_dict = {r.date: float(r.reading_value) for r in user_readings}
            
            # Sort dates to ensure correct order for calculation
            sorted_dates = sorted(readings_dict.keys())
            
            previous_value = None
            
            # If we need to calculate consumption (difference), we need to iterate through sorted dates
            # However, the chart expects data points aligned with the global 'dates' list.
            
            # Let's build a map of date -> value/consumption first
            consumption_map = {}
            
            if util_code in ['Cold Water', 'Hot Water', 'Heating']:
                # Calculate consumption: current - previous
                for i, d in enumerate(sorted_dates):


                    current_val = readings_dict[d]
                    if i == 0:
                        # First reading, consumption is 0 or undefined? 
                        # Usually 0 or we can't calculate consumption yet.
                        # Let's assume 0 for the very first reading or just the reading itself if it's a counter starting at 0?
                        # Typically for meters, the first reading is just a baseline.
                        # Let's set it to 0 for the chart.
                        consumption_map[d] = 0 
                    else:
                        prev_date = sorted_dates[i-1]
                        prev_val = readings_dict[prev_date]
                        consumption = current_val - prev_val
                        # Handle potential negative consumption (meter replacement or error)
                        consumption_map[d] = max(0, consumption)
            else:
                consumption_map = readings_dict


            # Now align with global dates
            for d in dates:
                if d in consumption_map:
                    data_points.append(consumption_map[d])
                else:
                    data_points.append(None)
            
            color = colors[color_index % len(colors)]

            dataset = {
                'label': f'{username} - {util_name}',
                'data': data_points,
                'backgroundColor': color,
                'borderColor': color,
                'borderWidth': 1
            }

            
            if util_code in ['Cold Water', 'Hot Water']:
                datasets_water.append(dataset)
            elif util_code == 'Energy':
                datasets_energy.append(dataset)
            elif util_code == 'Heating':
                datasets_heating.append(dataset)
                
            color_index += 1

    # Get available years for report dropdown
    available_years = sorted(list(set(readings.dates('date', 'year'))), reverse=True)
    available_years = [d.year for d in available_years]

    # Get available users
    available_users = sorted(list(set(readings.values_list('user__username', flat=True))))

    fee_rates = FeeRate.objects.all()

    context = {
        'readings': readings_table,
        'fee_rates': fee_rates,
        'available_years': available_years,
        'available_users': available_users,
        'chart_labels': formatted_dates,
        'datasets_water': datasets_water,
        'datasets_energy': datasets_energy,
        'datasets_heating': datasets_heating,
        'form': form,
        'fee_form': fee_form,
        'active_tab': active_tab,
    }
    return render(request, 'expenses/dashboard.html', context)

def delete_reading(request, pk):
    reading = get_object_or_404(MeterReading, pk=pk)
    if request.method == 'POST':
        reading.delete()
        messages.success(request, 'Entry deleted successfully!')
        return redirect(f"{reverse('dashboard')}?tab=History")
    return redirect('dashboard')

def edit_reading(request, pk):
    reading = get_object_or_404(MeterReading, pk=pk)
    if request.method == 'POST':
        form = MeterReadingForm(request.POST, instance=reading)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entry updated successfully!')
            return redirect(f"{reverse('dashboard')}?tab=History")
    else:
        form = MeterReadingForm(instance=reading)
    return render(request, 'expenses/edit_reading.html', {'form': form, 'reading': reading})

def delete_fee_rate(request, pk):
    fee = get_object_or_404(FeeRate, pk=pk)
    if request.method == 'POST':
        fee.delete()
        messages.success(request, 'Fee rate deleted successfully!')
        return redirect(f"{reverse('dashboard')}?tab=Fees")
    return redirect('dashboard')

def edit_fee_rate(request, pk):
    fee = get_object_or_404(FeeRate, pk=pk)
    if request.method == 'POST':
        form = FeeRateForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee rate updated successfully!')
            return redirect(f"{reverse('dashboard')}?tab=Fees")
    else:
        form = FeeRateForm(instance=fee)
    return render(request, 'expenses/edit_fee_rate.html', {'form': form, 'fee': fee})




