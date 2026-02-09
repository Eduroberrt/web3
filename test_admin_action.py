#!/usr/bin/env python
"""
Test admin action directly
Run with: python test_admin_action.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web3.settings')
django.setup()

from django.contrib.auth import get_user_model
from my_app.models import DepositTransaction, Wallet, Notification
from django.utils import timezone
from decimal import Decimal

User = get_user_model()

def test_admin_confirm_action():
    print("=" * 60)
    print("TESTING ADMIN CONFIRM ACTION DIRECTLY")
    print("=" * 60)
    
    # Get or create test user
    test_user = User.objects.first()
    if not test_user:
        print("ERROR: No users found")
        return
    
    print(f"\nUsing user: {test_user.username}")
    
    # Create a test pending deposit
    print("\n1. Creating test deposit...")
    test_deposit = DepositTransaction.objects.create(
        user=test_user,
        coin_type='bitcoin',
        amount=Decimal('250.00'),
        wallet_address='test_wallet_address',
        status='pending'
    )
    print(f"   Created: Deposit #{test_deposit.id}, Amount: ${test_deposit.amount}, Status: {test_deposit.status}")
    
    # Get initial balance
    print("\n2. Checking initial balance...")
    wallet, created = Wallet.objects.get_or_create(user=test_user)
    initial_balance = wallet.bitcoin_balance
    print(f"   Bitcoin balance before: ${initial_balance}")
    print(f"   Total balance before: ${wallet.total_balance}")
    
    # Simulate the admin action
    print("\n3. Simulating admin confirm action...")
    queryset = DepositTransaction.objects.filter(id=test_deposit.id, status='pending')
    print(f"   Queryset count: {queryset.count()}")
    
    updated = 0
    errors = []
    
    for transaction in queryset:
        try:
            print(f"\n   Processing transaction #{transaction.id}...")
            
            # Check amount
            if not transaction.amount or transaction.amount <= 0:
                error_msg = f"Transaction {transaction.id}: No amount set or amount is zero"
                errors.append(error_msg)
                print(f"   ERROR: {error_msg}")
                continue
            
            print(f"   Amount OK: ${transaction.amount}")
            
            # Get or create wallet
            wallet, wallet_created = Wallet.objects.get_or_create(user=transaction.user)
            print(f"   Wallet {'created' if wallet_created else 'found'}")
            
            # Add balance
            coin_type = transaction.coin_type
            amount = transaction.amount
            
            print(f"   Adding ${amount} to {coin_type}_balance...")
            print(f"   Current {coin_type}_balance: ${wallet.get_balance(coin_type)}")
            
            wallet.add_balance(coin_type, amount)
            
            # Verify update
            wallet.refresh_from_db()
            new_balance = wallet.get_balance(coin_type)
            print(f"   New {coin_type}_balance: ${new_balance}")
            
            if new_balance == initial_balance + amount:
                print(f"   ✓ Balance updated correctly!")
            else:
                print(f"   ✗ Balance mismatch! Expected ${initial_balance + amount}, got ${new_balance}")
            
            # Update transaction
            transaction.status = 'confirmed'
            transaction.confirmed_at = timezone.now()
            transaction.processed_by = test_user  # Using test_user as admin
            transaction.save()
            print(f"   Transaction status changed to: {transaction.status}")
            
            # Create notification
            notification = Notification.objects.create(
                user=transaction.user,
                type='deposit_confirmed',
                title='Deposit Confirmed ✓',
                message=f'Your {transaction.get_coin_type_display()} deposit of ${transaction.amount} has been confirmed and credited to your account.'
            )
            print(f"   Notification created: #{notification.id}")
            
            updated += 1
            
        except Exception as e:
            error_msg = f"Transaction {transaction.id}: {str(e)}"
            errors.append(error_msg)
            print(f"   ERROR: {error_msg}")
            import traceback
            traceback.print_exc()
    
    # Check final balance
    print("\n4. Checking final balance...")
    wallet.refresh_from_db()
    final_balance = wallet.bitcoin_balance
    print(f"   Bitcoin balance after: ${final_balance}")
    print(f"   Total balance after: ${wallet.total_balance}")
    print(f"   Expected increase: ${Decimal('250.00')}")
    print(f"   Actual increase: ${final_balance - initial_balance}")
    
    # Summary
    print("\n" + "=" * 60)
    if errors:
        print("ERRORS ENCOUNTERED:")
        for error in errors:
            print(f"  - {error}")
    
    if updated > 0:
        print(f"\n✓ SUCCESS: {updated} transaction(s) processed")
    else:
        print("\n✗ FAILED: No transactions were updated")
    print("=" * 60)
    
    # Cleanup
    print("\nCleanup:")
    test_deposit.delete()
    notification.delete()
    print("Test data deleted.")
    
    # Reset balance for next test
    wallet.bitcoin_balance = initial_balance
    wallet.save()
    print(f"Balance reset to ${initial_balance}")

if __name__ == '__main__':
    test_admin_confirm_action()
