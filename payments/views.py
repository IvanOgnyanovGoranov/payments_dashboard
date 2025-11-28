from django.shortcuts import render
from payments.services.analytics import (
    total_volume_per_account,
    payments_per_month,
    top_beneficiaries,
    status_breakdown,
)

def dashboard(request):
    # Query the analytics
    account_volumes = list(total_volume_per_account())
    monthly = list(payments_per_month())
    beneficiaries = list(top_beneficiaries())
    statuses = status_breakdown()

    # Prepare data for Chart.js
    months = [row['month'].strftime('%Y-%m') for row in monthly]
    monthly_amounts = [float(row['total_amount']) for row in monthly]

    context = {
        'account_volumes': account_volumes,
        'months': months,
        'monthly_amounts': monthly_amounts,
        'beneficiaries': beneficiaries,
        'statuses': statuses,
    }
    return render(request, 'payments/dashboard.html', context)