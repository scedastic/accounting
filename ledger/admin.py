from django.contrib import admin
from .models import Account, JournalEntry, JournalType, Transaction

class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'description', 'account_type', 'balance']
    readonly_fields = ['created_at', 'updated_at', 'slug']

    fieldsets = (
        ('Basic Information', {
            'fields': ('account_number', 'description', 'account_type', 'natural_balance', 'balance'),
         }),
        ('Time Stamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),   # Allows for collapsing this section on the admin page
        }),
        ('Unique', {
            'fields': ('slug',),
            'classes': ('collapse',),
        }),
    )
    list_filter = ['account_type', ]
    search_fields = ['description',]
    ordering = ['account_number',]


class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['transaction', 'account', 'debit_credit', 'amount'] 
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


class JournalTypeAdmin(admin.ModelAdmin):
    list_display = ['code','description',] 
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'description'), 
        }),
        ('Time Stamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description','transaction_date', 'post_date'] # 'is_posted',
    readonly_fields = ['created_at', 'updated_at', 'slug']
    ordering = ['transaction_date',]
    fieldsets = (
        ('Basic Information', {
            'fields': ('description', 'transaction_date',  'post_date'), #'is_posted',
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
admin.site.register(JournalType, JournalTypeAdmin)
admin.site.register(JournalEntry, JournalEntryAdmin)