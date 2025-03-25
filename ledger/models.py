import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

ACCOUNT_TYPES = [
    ('A', 'Asset' ),
    ('I','Inventory'),
    ('L', 'Liability' ),
    ('O', 'Owner Equity'),
    ('R', 'Revenue' ),
    ('E', 'Expense' ),
]

DEBIT_CREDIT = [
    ('D', 'Debit'),
    ('C', 'Credit'),
]

class Account(models.Model):
    account_number = models.CharField(max_length=25, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    account_type = models.CharField(choices=ACCOUNT_TYPES, blank=True, max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    natural_balance = models.CharField(choices=DEBIT_CREDIT, max_length=10)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)

    # Time Stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("account-detail", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.account_number}-{self.description}")
        return super(Account, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.account_number} - {self.description}"
    
class Transaction(models.Model):
    description = models.CharField(max_length=200, null=True, blank=True)
    transaction_date = models.DateField(null=True, blank=True, default=datetime.date.today)
    post_date = models.DateField(blank=True, null=True)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)

    # Time Stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Non-persistent fields
    debits = 0
    credits = 0

    def get_absolute_url(self):
        return reverse("transaction-detail", kwargs={"slug": self.slug})
    

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.description}{self.transaction_date}")
        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} | {self.transaction_date}"

    def post_transaction(self):
        if not self.is_balanced():
            raise ArithmeticError(f"Transaction is not balanced: debits: {self.debits}, credits: {self.credits}")
        
        for entry in self.entries.all():
            entry.post_entry()
        self.post_date = datetime.datetime.today        
        self.save()

    def is_balanced(self):
        """Recalculates the total debits and credits of the Journal Entries in this transaction and returns whether they are equal

        Returns:
            bool: `debits` == `credits`
        """
        self.debits = 0
        self.credits = 0

        for entry in self.entries.all():
            if entry.debit_credit=='D':
                self.debits += entry.amount 
            else:
                self.credits += entry.amount

        return self.debits == self.credits
    
    def is_posted(self):
        if self.entries.count() == 0:
            return False
        for entry in self.entries.all():
            if entry.is_posted == False:
                return False
        return True

class JournalType(models.Model):
    code = models.CharField(max_length=10, null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    sort_order = models.IntegerField(default=99)

    # Time Stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.code} - {self.description}"
    class Meta:
        verbose_name_plural = "Journal Types"
        ordering = ['sort_order',]


class JournalEntry(models.Model):
    debit_credit = models.CharField(choices=DEBIT_CREDIT, max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_posted = models.BooleanField(default=False)

    journal_type = models.ManyToManyField(JournalType)
    account = models.ForeignKey(Account,  on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, related_name='entries', on_delete=models.CASCADE)

    # Time Stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def credit_amount(self):
        if self.debit_credit == 'C':
            return self.amount
        return 0
    
    def debit_amount(self):
        if self.debit_credit == 'D':
            return self.amount
        return 0

    def post_entry(self):
        """Make change to the account referenced. Mark the entry as posted with current date.
        IF the account referenced is a natural debit account and this is a debit entry 
            OR the account is a natural credit account and this is a credit entry, 
        THEN increase the account's balance by the amount.
        IF the account referenced is a natural debit account and this is a credit entry 
            OR the account is a natural credit account and this is a debit entry, 
        THEN decrease the account's balance by the amount.
        
        """
        if self.is_posted:
            return 
        if self.debit_credit == self.account.natural_balance:
            self.account.balance += self.amount
        else:
            self.account.balance -= self.amount
        self.post_date = datetime.date.today
        self.is_posted = True
        self.save()


    def __str__(self):
        return f"{self.transaction.description} - {self.account.description}"
    class Meta:
        verbose_name_plural = "Journal Entries"