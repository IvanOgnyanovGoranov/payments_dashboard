from django.contrib import admin

from payments.models import Company, Customer, Account, Payment


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'customer_code',
        'created_at',
        'contact_email',
    )

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'company_code',
        'created_at',
        'address',
        'customer',
    )
    list_filter = (
        'customer',
    )


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
        'iban',
        'account_number',
        'currency',
        'is_active',
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'reference',
        'amount',
        'payment_date',
        'account',
        'beneficiary_name',
    )
    list_filter = ('account', 'payment_date')
