from django.db import models
from django.db.models import Q
from django.db.models.constraints import CheckConstraint
from payments.utils.references import generate_payment_reference

CURRENCY_CHOICES = [
    ("EUR", "Euro"),
    ("USD", "US Dollar"),
    ("GBP", "British Pound"),
]

class Customer(models.Model):
    """Represents companies and accounts within a contract."""
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    customer_code = models.PositiveIntegerField(
        unique=True,
    )

    contact_email = models.EmailField(
        max_length=100,
    )
    created_at = models.DateField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name


class Company(models.Model):
    """Represents a company within a contract."""
    customer = models.ForeignKey(
        to=Customer,
        on_delete=models.CASCADE,
        related_name="companies",
    )

    name = models.CharField(
        max_length=100,
    )

    company_code = models.PositiveIntegerField(
        unique=True,
    )

    created_at = models.DateField(
        auto_now_add=True,
    )

    address = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "name"],
                name="unique_company_per_customer"
            )
        ]

    def __str__(self):
        return self.name


class Account(models.Model):
    """Represent and account that has a Company as an owner."""

    company = models.ForeignKey(
        to=Company,
        on_delete=models.CASCADE,
        related_name='accounts'
    )

    display_name = models.CharField(
        max_length=100,
    )

    iban = models.CharField(
        null=True,
        blank=True,
        max_length=34,
    )

    account_number = models.CharField(
        null=True,
        blank=True,
        max_length=50,
    )

    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(iban__isnull=False, iban__gt='') | Q(account_number__isnull=False, account_number__gt=''),
                name="iban_or_account_required"
            ),
            models.UniqueConstraint(
                fields=["company", "display_name"],
                name="unique_account_per_company"
            )
        ]

    def __str__(self):
        return self.display_name


class Payment(models.Model):
    """Represent all payments including imported, entered manually or a part of a batch."""
    STATUS_CHOICES = [
        ('Processed', 'Processed'),
        ('Failed', 'Failed'),
        ('In Progress', 'In Progress'),
    ]

    account = models.ForeignKey(
        to=Account,
        on_delete=models.CASCADE,
        related_name='payments',
    )

    beneficiary_name = models.CharField(
        max_length=200,
    )

    beneficiary_account_number = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
    )

    payment_date = models.DateTimeField()

    status = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        default='In Progress',
    )

    is_batch = models.BooleanField(
        default=False,
    )

    reference = models.CharField(
        max_length=30,
        unique=True,
        default=generate_payment_reference,
        editable=False
    )

    class Meta:
        indexes = [
            models.Index(fields=['payment_date']),
            models.Index(fields=['status']),
            models.Index(fields=['currency']),
            models.Index(fields=['account', 'payment_date']),
        ]

    def __str__(self):
        return f"Payment {self.reference} - {self.status} {self.amount} {self.currency}"

