from django.contrib import admin
from .models import Account, JournalEntry, Transaction

class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'description', 'account_type', 'balance']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('account_number', 'description', 'account_type', 'natural_balance', 'balance'),
         }),
        ('Time Stamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    list_filter = ['account_type', ]
    search_fields = ['description',]
    ordering = ['account_number',]


class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['journal_type', 'transaction', 'account', 'debit_credit', 'amount']
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['transaction__description', 'account__description']
    fieldsets = (
        ('Basic Information', {
            'fields': ('journal_type', 'debit_credit', 'amount'),
        }),
         ('Related Fields', {
             'fields': ('transaction', 'account'), 
         }),
        ('Time Stamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    list_filter = ['journal_type', 'account']
    search_fields = ['transaction',]
    ordering = ['updated_at', '-debit_credit']

class JournalEntryInline(admin.TabularInline):
    model = JournalEntry

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description','transaction_date', 'is_posted', 'post_date']
    readonly_fields = ['created_at', 'updated_at', 'slug']
    ordering = ['transaction_date',]
    fieldsets = (
        ('Basic Information', {
            'fields': ('description', 'transaction_date', 'is_posted', 'post_date'),
         }),
        ('Time Stamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
        ('Unique', {
            'fields': ('slug',),
            'classes': ('collapse',),
        }),
    )
    inlines = [JournalEntryInline,]

admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(JournalEntry, JournalEntryAdmin)