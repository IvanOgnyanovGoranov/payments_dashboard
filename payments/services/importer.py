import csv
from decimal import Decimal, InvalidOperation
from datetime import datetime
from payments.models import Payment


def validate_and_convert(payment):
    """Validates and converts payment fields. Raises ValueError on any issue."""

    try:
        payment['amount'] = Decimal(payment['amount'])
    except (InvalidOperation, ValueError):
        raise ValueError(f"Invalid amount: {payment['amount']}")

    try:
        payment['payment_date'] = datetime.strptime(payment["payment_date"], "%Y-%m-%d")
    except (ValueError, TypeError):
        raise ValueError(f"Invalid payment_date: {payment['payment_date']}")

    payment["is_batch"] = str(payment["is_batch"]).lower() == "true"

    return payment


def load_payments_from_csv(filepath):
    """Reads a CSV file and returns a list of validated payment dictionaries."""
    payments = []

    with open(filepath, newline="", encoding="utf-8") as data_file:
        reader = csv.reader(data_file)
        header = next(reader, None)

        for row in reader:
            if not row:
                continue

            payment = {header[i]: row[i] for i in range(len(row))}

            try:
                validate_and_convert(payment)
            except ValueError as e:
                print("[SKIPPING ROW]", e)
                continue

            payments.append(payment)

    print(payments)
    return payments

payments_list = load_payments_from_csv('payments/imports/payments_demo.csv')

def save_payments_to_db(payments_list):
    payment_objects = []
    skipped = 0

    for payment_dict in payments_list:
        try:
            payment_objects.append(Payment(**payment_dict))

        except Exception as e:
            print(f"[SKIP] Invalid payment data: {e}")
            skipped += 1

    print(f"Inserted: {len(payment_objects)}")
    print(f"Skipped: {skipped}")