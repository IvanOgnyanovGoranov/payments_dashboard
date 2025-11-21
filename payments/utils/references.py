import uuid

def generate_payment_reference():
    return f"PMT-{uuid.uuid4().hex[:10].upper()}"
