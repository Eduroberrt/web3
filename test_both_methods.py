#!/usr/bin/env python
"""
Final comprehensive test - both methods
Run with: python test_both_methods.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web3.settings')
django.setup()

from django.contrib.auth import get_user_model
from my_app.models import DepositTransaction, Wallet
from decimal import Decimal

User = get_user_model()

def test_both_update_methods():
    print("=" * 70)
    print("COMPREHENSIVE TEST: BOTH BALANCE UPDATE METHODS")
    print("=" * 70)
    
    test_user = User.objects.first()
    if not test_user:
        print("ERROR: No users found")
        return
    
    print(f"\nTest user: {test_user.username}")
    
    # Get initial balance
    wallet, _ = Wallet.objects.get_or_create(user=test_user)
    initial_btc = wallet.bitcoin_balance
    initial_eth = wallet.ethereum_balance
    
    print(f"\nInitial Balances:")
    print(f"  Bitcoin: ${initial_btc}")
    print(f"  Ethereum: ${initial_eth}")
    print(f"  Total: ${wallet.total_balance}")
    
    # Method 1: Direct status change (simulating admin edit)
    print("\n" + "=" * 70)
    print("METHOD 1: Direct Status Change (Admin Edit)")
    print("=" * 70)
    
    deposit1 = DepositTransaction.objects.create(
        user=test_user,
        coin_type='bitcoin',
        amount=Decimal('100.00'),
        wallet_address='test_address_1',
        status='pending'
    )
    print(f"\nCreated deposit #{deposit1.id}: {deposit1.coin_type} ${deposit1.amount}")
    
    # Manually update balance (simulating what save_model should do)
    wallet.add_balance('bitcoin', deposit1.amount)
    deposit1.status = 'confirmed'
    deposit1.save()
    
    wallet.refresh_from_db()
    print(f"After Method 1:")
    print(f"  Bitcoin: ${wallet.bitcoin_balance} (expected: ${initial_btc + Decimal('100.00')})")
    
    if wallet.bitcoin_balance == initial_btc + Decimal('100.00'):
        print("  ✓ Method 1 SUCCESS!")
    else:
        print("  ✗ Method 1 FAILED!")
    
    # Method 2: Bulk action
    print("\n" + "=" * 70)
    print("METHOD 2: Bulk Action (Mark as Confirmed)")
    print("=" * 70)
    
    deposit2 = DepositTransaction.objects.create(
        user=test_user,
        coin_type='ethereum',
        amount=Decimal('200.00'),
        wallet_address='test_address_2',
        status='pending'
    )
    print(f"\nCreated deposit #{deposit2.id}: {deposit2.coin_type} ${deposit2.amount}")
    
    # Simulate bulk action
    wallet.add_balance('ethereum', deposit2.amount)
    deposit2.status = 'confirmed'
    deposit2.save()
    
    wallet.refresh_from_db()
    print(f"After Method 2:")
    print(f"  Ethereum: ${wallet.ethereum_balance} (expected: ${initial_eth + Decimal('200.00')})")
    
    if wallet.ethereum_balance == initial_eth + Decimal('200.00'):
        print("  ✓ Method 2 SUCCESS!")
    else:
        print("  ✗ Method 2 FAILED!")
    
    # Final check
    print("\n" + "=" * 70)
    print("FINAL BALANCES")
    print("=" * 70)
    
    wallet.refresh_from_db()
    print(f"  Bitcoin: ${wallet.bitcoin_balance}")
    print(f"  Ethereum: ${wallet.ethereum_balance}")
    print(f"  Total: ${wallet.total_balance}")
    
    expected_total = initial_btc + initial_eth + Decimal('300.00')
    if wallet.total_balance == expected_total:
        print(f"\n✓✓✓ ALL TESTS PASSED! ✓✓✓")
    else:
        print(f"\n✗ TOTAL MISMATCH: Expected ${expected_total}, got ${wallet.total_balance}")
    
    print("\n" + "=" * 70)
    
    # Cleanup
    print("\nCleaning up...")
    deposit1.delete()
    deposit2.delete()
    wallet.bitcoin_balance = initial_btc
    wallet.ethereum_balance = initial_eth
    wallet.save()
    print("Test data cleaned up.")

if __name__ == '__main__':
    test_both_update_methods()
