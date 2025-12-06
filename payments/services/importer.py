import csv
import os
from decimal import Decimal
from django.conf import settings
from datetime import datetime


def load_payments_from_csv(filepath):
    """Reads a CSV file and returns a list of validated payment dictionaries."""
    payments = []

    with open(filepath, newline="", encoding="utf-8") as data_file:
        reader = csv.reader(data_file)

        header = next(reader, None)

        for row in reader:
            if not row:
                continue

            reference = row[0]
            raw_amount = row[1]
            raw_date = row[2]
            account_number = row[3]
            beneficiary_name = row[4]
            beneficiary_account_number = row[5]

            try:
                amount = Decimal(raw_amount)
            except:
                print(f"[SKIPPING ROW] Invalid amount: {raw_amount}")
                continue

            try:
                payment_date = datetime.strptime(raw_date, '%Y-%m-%d')
            except:
                print(f"[SKIPPING ROW] Invalid date: {raw_date}")
                continue

            payment = {
                    "account_number": account_number,
                    "beneficiary_name": beneficiary_name,
                    "beneficiary_account_number": beneficiary_account_number,
                    "amount": raw_amount,
                    "currency": "EUR",
                    "payment_date": raw_date,
                    "status": "Processed",
                    "is_batch": False,
                    "reference": reference
            }
            payments.append(payment)

    return payments



