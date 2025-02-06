from django.db import models

ACCOUNT_TYPES = [
    ('A', 'Asset' ),
    ('L', 'Liability' ),
    ('O', "Owner Equity" ),
    ('R', 'Revenue' ),
    ('E', 'Expense' ),
]

DEBIT_CREDIT = [
    ('D', 'Debit'),
    ('C', 'Credit'),
]

JOURNAL_TYPE = [
    ('GJ', 'General'),
    ('AR', 'AR'),
    ('AP', 'AP'),
    ('SJ', 'SJ'),
    ('PJ', 'PJ'),
]
class Account(models.Model):
    account_number = models.CharField(max_length=25, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    account_type = models.CharField(choices=ACCOUNT_TYPES, blank=True, max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Time Stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_number} - {self.description}"
    
class Transaction(models.Model):
    description = models.CharField(max_length=200, null=True, blank=True)
    transaction_date = models.DateField(auto_now_add=True)
    # Time Stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description} @ {self.transaction_date}"

class JournalEntry(models.Model):
    journal_type = models.CharField(choices=JOURNAL_TYPE, default="GJ", max_length=20)
    debit_credit = models.CharField(choices=DEBIT_CREDIT, max_length=10)
    is_posted = models.BooleanField(default=False)
    post_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    account = models.ForeignKey(Account,  on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    # Time Stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "Journal Entries"