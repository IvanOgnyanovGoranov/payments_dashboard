import csv
from decimal import Decimal, InvalidOperation
from datetime import datetime

from payments.models import Payment

def validate_and_convert(payment):
    """Validates and converts payment's amount, date and is_batch, and returns errors if there are any."""
    errors = []

    try:
        payment['amount'] = Decimal(payment['amount'])
    except (InvalidOperation, ValueError):
        errors.append('Invalid amount')

    try:
        payment['payment_date'] = datetime.strptime(payment["payment_date"])
    except (ValueError, TypeError):
        errors.append("Invalid payment_date")

        # is_batch
    try:
        payment["is_batch"] = str(payment["is_batch"]).lower() == "true"
    except Exception:
        errors.append("Invalid is_batch")

    return payment, errors


def load_payments_from_csv(filepath):
    """Reads a CSV file and returns a list of validated payment dictionaries."""
    payments = []

    with open(filepath, newline="", encoding="utf-8") as data_file:
        reader = csv.reader(data_file)

        header = next(reader, None)

        for row in reader:
            if not row:
                continue

            payment = {}

            for position in range(len(row)):
                key = header[position]
                value = row[position]
                payment[key] = value

            payment["amount"] = Decimal(payment["amount"])
            payment["payment_date"] = datetime.strptime(payment["payment_date"], "%Y-%m-%d")
            payment["is_batch"] = payment["is_batch"].lower() == "true"

            payments.append(payment)

    return payments

payments_list = load_payments_from_csv('payments/imports/payments_demo.csv')

def save_payments_to_db(payments_list):
    created = 0
    skipped = 0

    for payment_dict in payments_list:
        try:
            Payment.objects.create(**payment_dict)
            created += 1

        except Exception as e:
            print(f"[SKIP] Could not insert payment {payment_dict.get('reference')}: {e}")
            skipped += 1
            continue

    print(f"Inserted: {created}")
    print(f"Skipped: {skipped}")