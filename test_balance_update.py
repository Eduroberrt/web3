#!/usr/bin/env python
"""
Test script to diagnose balance update issues
Run with: python test_balance_update.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web3.settings')
django.setup()

from django.contrib.auth import get_user_model
from my_app.models import DepositTransaction, Wallet
from decimal import Decimal

User = get_user_model()

def test_balance_update():
    print("=" * 60)
    print("BALANCE UPDATE DIAGNOSTIC TEST")
    print("=" * 60)
    
    # Step 1: Check if there are any users
    print("\n1. Checking users...")
    users = User.objects.all()
    print(f"   Total users: {users.count()}")
    
    if users.count() == 0:
        print("   ERROR: No users found. Please create a user first.")
        return
    
    test_user = users.first()
    print(f"   Using test user: {test_user.username} (ID: {test_user.id})")
    
    # Step 2: Check/Create wallet
    print("\n2. Checking wallet...")
    wallet, created = Wallet.objects.get_or_create(user=test_user)
    print(f"   Wallet {'created' if created else 'already exists'}")
    print(f"   Current Bitcoin balance: ${wallet.bitcoin_balance}")
    print(f"   Current Ethereum balance: ${wallet.ethereum_balance}")
    print(f"   Current Total balance: ${wallet.total_balance}")
    
    # Step 3: Check deposit transactions
    print("\n3. Checking deposit transactions...")
    pending_deposits = DepositTransaction.objects.filter(user=test_user, status='pending')
    print(f"   Pending deposits: {pending_deposits.count()}")
    
    confirmed_deposits = DepositTransaction.objects.filter(user=test_user, status='confirmed')
    print(f"   Confirmed deposits: {confirmed_deposits.count()}")
    
    # Step 4: Create a test deposit if none exists
    print("\n4. Creating test deposit...")
    test_deposit = DepositTransaction.objects.create(
        user=test_user,
        coin_type='bitcoin',
        amount=Decimal('100.00'),
        wallet_address='test_address_12345',
        status='pending'
    )
    print(f"   Created deposit ID: {test_deposit.id}")
    print(f"   Coin type: {test_deposit.coin_type}")
    print(f"   Amount: ${test_deposit.amount}")
    
    # Step 5: Test the add_balance method
    print("\n5. Testing add_balance method...")
    print(f"   Before: bitcoin_balance = ${wallet.bitcoin_balance}")
    
    try:
        wallet.add_balance('bitcoin', Decimal('100.00'))
        wallet.refresh_from_db()
        print(f"   After: bitcoin_balance = ${wallet.bitcoin_balance}")
        print(f"   SUCCESS: Balance updated correctly!")
    except Exception as e:
        print(f"   ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Step 6: Test total_balance property
    print("\n6. Testing total_balance property...")
    wallet.refresh_from_db()
    print(f"   Bitcoin: ${wallet.bitcoin_balance}")
    print(f"   Ethereum: ${wallet.ethereum_balance}")
    print(f"   XRP: ${wallet.xrp_balance}")
    print(f"   Total: ${wallet.total_balance}")
    
    # Step 7: Check field names match
    print("\n7. Checking field name mapping...")
    coin_types = ['bitcoin', 'ethereum', 'xrp', 'solana', 'usdt', 'xlm', 
                  'shiba', 'usdc', 'doge', 'ada', 'dot', 'trx']
    
    for coin in coin_types:
        field_name = f"{coin}_balance"
        has_field = hasattr(wallet, field_name)
        print(f"   {coin:10} -> {field_name:20} {'✓ EXISTS' if has_field else '✗ MISSING'}")
    
    print("\n" + "=" * 60)
    print("DIAGNOSTIC TEST COMPLETE")
    print("=" * 60)
    
    # Cleanup test deposit
    print("\nCleaning up test deposit...")
    test_deposit.delete()
    print("Test deposit deleted.")

if __name__ == '__main__':
    test_balance_update()
