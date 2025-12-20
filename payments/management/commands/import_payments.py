from django.core.management.base import BaseCommand
from payments.services.importer import import_payments


class Command(BaseCommand):
    help = "Import payments from a CSV file"

    def handle(self, *args, **options):
        import_payments("payments/imports/payments_demo.csv")

