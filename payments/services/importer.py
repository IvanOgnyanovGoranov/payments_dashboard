import csv
from decimal import Decimal, InvalidOperation
from datetime import datetime
from payments.models import Payment, Account


def validate_and_convert(payment):
    """Validates and converts payment fields. Raises ValueError on any issue."""

    try:
        payment['amount'] = Decimal(payment['amount'])
    except (InvalidOperation, ValueError):
        raise ValueError(f"Invalid amount: {payment['amount']}")

    try:
        payment['payment_date'] = datetime.strptime(payment["payment_date"], "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        raise ValueError(f"Invalid payment_date: {payment['payment_date']}")

    try:
        payment["account"] = Account.objects.get(display_name=payment["account"])
    except Account.DoesNotExist:
        raise ValueError(f"Unknown account: {payment['account']}")

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


def save_payments_to_db(payments_list):
    """Validates payment objects and bulk saves in the database."""
    payment_objects = []
    skipped = 0

    for payment_dict in payments_list:
        try:
            payment_objects.append(Payment(**payment_dict))

        except Exception as e:
            print(f"[SKIP] Invalid payment data: {e}")
            skipped += 1

    Payment.objects.bulk_create(payment_objects)

    print(f"Skipped: {skipped}")


def import_payments(filepath):
    """Triggers load_payments_from_csv and save_payments_to_db."""
    payments = load_payments_from_csv(filepath)
    save_payments_to_db(payments)
