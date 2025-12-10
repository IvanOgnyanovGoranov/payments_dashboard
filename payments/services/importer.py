import csv
from decimal import Decimal
from datetime import datetime

from payments.models import Payment


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

            # reference = row[0]
            # account_number = row[1]
            # beneficiary_name = row[2]
            # beneficiary_account_number = row[3]
            # raw_amount = row[4]
            # currency = row[5]
            # raw_date = row[6]
            # status = row[7]
            # is_batch = row[8]
            #
            # try:
            #     amount = Decimal(raw_amount)
            # except:
            #     print(f"[SKIPPING ROW] Invalid amount: {raw_amount}")
            #     continue
            #
            # try:
            #     payment_date = datetime.strptime(raw_date, '%Y-%m-%d')
            # except:
            #     print(f"[SKIPPING ROW] Invalid date: {raw_date}")
            #     continue
            #
            # payment = {
            #         "account_number": account_number,
            #         "beneficiary_name": beneficiary_name,
            #         "beneficiary_account_number": beneficiary_account_number,
            #         "amount": raw_amount,
            #         "currency": currency,
            #         "payment_date": raw_date,
            #         "status": status,
            #         "is_batch": is_batch,
            #         "reference": reference
            # }
            # payments.append(payment)
    print(payments)

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