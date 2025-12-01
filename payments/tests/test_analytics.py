from django.db.models.functions import datetime
from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from payments.models import Customer, Company, Account, Payment
from payments.services.analytics import payments_per_month


class AnalyticsTest(TestCase):
    def setUp(self):
        c = Customer.objects.create(name='C1', customer_code=1, contact_email='a@a.com')
        comp = Company.objects.create(customer=c, name='Co1', company_code=1, address='X')
        acc = Account.objects.create(company=comp, display_name='Acc1', account_number='123', currency='EUR')
        # create payments in two months
        Payment.objects.create(account=acc, beneficiary_name='B1', beneficiary_account_number='B1acc',
                               amount=Decimal('100.00'), currency='EUR',
                               payment_date=timezone.make_aware(datetime.datetime(2025, 1, 5, 12, 0, 0)),
                               status='Processed')
        Payment.objects.create(account=acc, beneficiary_name='B2', beneficiary_account_number='B2acc',
                               amount=Decimal('200.00'), currency='EUR',
                               payment_date=timezone.make_aware(datetime.datetime(2025, 2, 6, 12, 0, 0)),
                               status='Processed')

    def test_payments_per_month(self):
        rows = list(payments_per_month())
        print(rows)
        self.assertEqual(len(rows), 2)
        months = [r['month'].month for r in rows]
        self.assertIn(1, months)
        self.assertIn(2, months)
