from django.contrib import admin
from .models import Account, JournalEntry, Transaction

class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'description', 'account_type', 'balance']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('account_number', 'description', 'account_type', 'balance'),
         }),
        ('Time Stamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    list_filter = ['account_type', ]
    search_fields = ['description',]
    ordering = ['account_number',]


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description', 'transaction_date']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-transaction_date',]
    fieldsets = (
        ('Basic Information', {
            'fields': ('description', 'transaction_date'),
         }),
        ('Time Stamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['journal_type', 'transaction', 'account', 'debit_credit', 'amount']
    readonly_fields = ['created_at', 'updated_at', 'is_posted', 'post_date']
    search_fields = ['transaction__description', 'account__description']
    fieldsets = (
        ('Basic Information', {
            'fields': ('journal_type', 'debit_credit', 'is_posted', 'post_date', 'amount'),
        }),
         ('Related Fields', {
             'fields': ('transaction', 'account'), 
         }),
        ('Time Stamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(JournalEntry, JournalEntryAdmin)