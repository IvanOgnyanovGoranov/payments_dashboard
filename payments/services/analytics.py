from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth

from payments.models import Payment, Account

def total_volume_per_account(limit=50):
    """
    Returns QuerySet of dicts: account id/name and total_volume.
    Example result item: {'account__display_name': 'Main', 'total_volume': Decimal('12345.00')}
    """
    return (
        Payment.objects
        .values('account__id', 'account__display_name')
        .annotate(total_volume=Sum('amount'), payments_count=Count('id'))
        .order_by('-total_volume')[:limit]
    )

def payments_per_month():
    """
    Returns QuerySet grouped by month with total_amount and count.
    Each row: {'month': datetime(...), 'total_amount': Decimal(...), 'count': int}
    """
    return (
        Payment.objects
        .annotate(month=TruncMonth('payment_date'))
        .values('month')
        .annotate(total_amount=Sum('amount'), count=Count('id'))
        .order_by('month')
    )

def top_beneficiaries(limit=10):
    """
    Returns top beneficiaries by total amount.
    Each row: {'beneficiary_name': 'Acme', 'total_amount': Decimal(...), 'count': int}
    """
    return (
        Payment.objects
        .values('beneficiary_name')
        .annotate(total_amount=Sum('amount'), count=Count('id'))
        .order_by('-total_amount')[:limit]
    )

def status_breakdown():
    """
    Returns a dict-like list of {'status': 'Processed', 'count': X}
    """
    qs = (
        Payment.objects
        .values('status')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    return list(qs)