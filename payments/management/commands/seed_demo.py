from django.core.management.base import BaseCommand
from decimal import Decimal
import datetime

from payments.models import Customer, Company, Account, Payment

class Command(BaseCommand):
    help = "Seed demo data: 1 customer, 2 companies, 2 accounts, payments over 3 months."

    def handle(self, *args, **options):
        Payment.objects.all().delete()
        Account.objects.all().delete()
        Company.objects.all().delete()
        Customer.objects.all().delete()

        c = Customer.objects.create(name="DemoCorp", customer_code=1, contact_email="demo@corp.test")
        comp_a = Company.objects.create(customer=c, name="DemoCorp BE", company_code=1, address="Belgium")
        comp_b = Company.objects.create(customer=c, name="DemoCorp NL", company_code=2, address="Netherlands")

        acc1 = Account.objects.create(company=comp_a, display_name="Main EUR", account_number="BE123", currency="EUR")
        acc2 = Account.objects.create(company=comp_b, display_name="Main USD", account_number="NL321", currency="USD")

        base = datetime.datetime(2025, 1, 5, 12, 0, 0)
        payments = [
            (acc1, "Alice", "ALICEIBAN", Decimal("100.00"), base),
            (acc1, "Bob", "BOBIBAN", Decimal("250.00"), base + datetime.timedelta(days=40)),  # Feb
            (acc2, "Charlie", "CHARIBAN", Decimal("300.00"), base + datetime.timedelta(days=70)), # Mar
            (acc2, "Alice", "ALICEIBAN", Decimal("150.00"), base + datetime.timedelta(days=80)),  # Mar
        ]

        for acc, ben, ben_acc, amt, pdate in payments:
            Payment.objects.create(
                account=acc,
                beneficiary_name=ben,
                beneficiary_account_number=ben_acc,
                amount=amt,
                currency=acc.currency,
                payment_date=pdate,
                status='Processed'
            )

        self.stdout.write(self.style.SUCCESS("Seeded demo data."))
