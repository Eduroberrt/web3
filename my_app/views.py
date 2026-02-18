from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    """Home page view with all sections"""
    return render(request, 'home.html')

def connect(request):
    """Connect wallet page view"""
    return render(request, 'connect.html')

def backup_success(request):
    """Backup success page view"""
    return render(request, 'backup-success.html')

def login(request):
    """Login page view"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to authenticate with email as username
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'login.html')

def signup(request):
    """Signup page view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'signup.html')
        
        # Check if user already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'signup.html')
        
        # Split name into first and last name
        name_parts = name.strip().split(maxsplit=1)
        first_name = name_parts[0] if name_parts else ''
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Create new user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Log the user in
        auth_login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('dashboard')
    
    return render(request, 'signup.html')

@login_required(login_url='/login/')
def dashboard(request):
    """Dashboard page view"""
    from .models import KYCVerification, Wallet
    
    # Get or create KYC verification record
    kyc, created = KYCVerification.objects.get_or_create(user=request.user)
    
    # Get or create user wallet
    wallet, wallet_created = Wallet.objects.get_or_create(user=request.user)
    
    context = {
        'kyc': kyc,
        'wallet': wallet,
        'total_balance': wallet.total_balance,
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='/login/')
def profile(request):
    """Profile page view"""
    return render(request, 'profile.html')

@login_required(login_url='/login/')
def send(request):
    """Send funds page view"""
    return render(request, 'send.html')

@login_required(login_url='/login/')
def receive(request):
    """Receive funds page view"""
    if request.method == 'POST':
        coin = request.POST.get('coin')
        if coin:
            # Define wallet addresses for each coin
            coin_addresses = {
                'bitcoin': 'bc1q2xekqjvkdgskms70rcwxtz2cx7kxst8jvn7d5j',
                'xrp': 'rMAqM3QKp5GyjfvARv3AmRii6X1e87FLLj',
                'ethereum': '0xB564FA8A7277f5BfBb995F3CAa5E9157057b632B',
                'solana': 'Kf6TZgVVJnAGLpYxUJGqx71VMURWQzM4wFmprGdbWst',
                'usdt': '0xB564FA8A7277f5BfBb995F3CAa5E9157057b632B',
                'xlm': 'GA3BD7BIZTQM4EF2NINXK7PBMFN66UTZ4ORVQT3IWTATBGCNJ7X7WULD',
                'shiba': '0xB564FA8A7277f5BfBb995F3CAa5E9157057b632B',
                'usdc': '0xB564FA8A7277f5BfBb995F3CAa5E9157057b632B',
                'doge': 'DHUfr1Z4d6kNcbduzVVAkq15gzsNCAiYj5',
                'ada': 'addr1qysn9wqy92234vypjucezjttrqe54zw6refauhluvq7n9tgvvver6qlrx02zc3dk55twmnykec5kzaxtf0q8ramhnkqszrjfxa',
                'dot': '12VsN9TAPHjJxMEseZAtE3FsiuHLTvHMU7Q2nZ4vuNSwunkQ',
                'trx': 'TUgFkhoaVdcEVHpeMnYmYjYFZhEMJzSRQH'
            }
            
            # Create deposit transaction with pending status and wallet address
            from .models import DepositTransaction
            wallet_address = coin_addresses.get(coin, '')
            transaction = DepositTransaction.objects.create(
                user=request.user,
                coin_type=coin,
                wallet_address=wallet_address,
                status='pending'
            )
            # Return JSON for AJAX or redirect
            from django.http import JsonResponse
            return JsonResponse({'success': True, 'coin': coin})
    
    # Get user's receive transactions for history table
    from .models import DepositTransaction
    transactions = DepositTransaction.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'receive.html', {'transactions': transactions})

@login_required(login_url='/login/')
def receive_detail(request, coin=None):
    """Receive detail page view for specific coin"""
    # If coin is from GET parameter (from dropdown)
    if not coin:
        coin = request.GET.get('coin', '')
    
    coin_data = {
        'bitcoin': {
            'name': 'Bitcoin',
            'symbol': 'BTC',
            'address': 'bc1q2xekqjvkdgskms70rcwxtz2cx7kxst8jvn7d5j'
        },
        'xrp': {
            'name': 'Ripple',
            'symbol': 'XRP',
            'address': 'rMAqM3QKp5GyjfvARv3AmRii6X1e87FLLj'
        },
        'ethereum': {
            'name': 'Ethereum',
            'symbol': 'ETH',
            'address': '0xB564FA8A7277f5BfBb995F3CAa5E9157057b632B'
        },
        'solana': {
            'name': 'Solana',
            'symbol': 'SOL',
            'address': 'Kf6TZgVVJnAGLpYxUJGqx71VMURWQzM4wFmprGdbWst'
        },
        'usdt': {
            'name': 'Tether',
            'symbol': 'USDT',
            'address': '0xB564FA8A7277f5BfBb995F3CAa5E9157057b632B'
        },
        'xlm': {
            'name': 'Stellar Lumen',
            'symbol': 'XLM',
            'address': 'GA3BD7BIZTQM4EF2NINXK7PBMFN66UTZ4ORVQT3IWTATBGCNJ7X7WULD'
        },
        'shiba': {
            'name': 'Shiba Inu',
            'symbol': 'SHIB',
            'address': '0xB564FA8A7277f5BfBb995F3CAa5E9157057b632B'
        },
        'usdc': {
            'name': 'USD Coin',
            'symbol': 'USDC',
            'address': '0xB564FA8A7277f5BfBb995F3CAa5E9157057b632B'
        },
        'doge': {
            'name': 'Dogecoin',
            'symbol': 'DOGE',
            'address': 'DHUfr1Z4d6kNcbduzVVAkq15gzsNCAiYj5'
        },
        'ada': {
            'name': 'Cardano',
            'symbol': 'ADA',
            'address': 'addr1qysn9wqy92234vypjucezjttrqe54zw6refauhluvq7n9tgvvver6qlrx02zc3dk55twmnykec5kzaxtf0q8ramhnkqszrjfxa'
        },
        'dot': {
            'name': 'Polkadot',
            'symbol': 'DOT',
            'address': '12VsN9TAPHjJxMEseZAtE3FsiuHLTvHMU7Q2nZ4vuNSwunkQ'
        },
        'trx': {
            'name': 'Tron',
            'symbol': 'TRX',
            'address': 'TUgFkhoaVdcEVHpeMnYmYjYFZhEMJzSRQH'
        }
    }
    
    selected_coin = coin_data.get(coin.lower(), {
        'name': coin.title(),
        'symbol': coin.upper(),
        'address': 'Address not available'
    })
    
    context = {
        'coin_name': selected_coin['name'],
        'coin_symbol': selected_coin['symbol'],
        'wallet_address': selected_coin['address'],
        'coin': coin
    }
    return render(request, 'receive_detail.html', context)

@login_required(login_url='/login/')
def verify(request):
    """KYC verification page view"""
    from .models import KYCVerification
    from django.utils import timezone
    
    # Get or create KYC verification record
    kyc, created = KYCVerification.objects.get_or_create(user=request.user)
    
    show_success_modal = False
    
    if request.method == 'POST':
        # Handle KYC submission
        document_type = request.POST.get('document_type')
        document_file = request.FILES.get('document')
        
        if document_type and document_file:
            kyc.document_type = document_type
            kyc.document_file = document_file
            kyc.status = 'pending'
            kyc.submitted_at = timezone.now()
            kyc.save()
            
            show_success_modal = True
        else:
            messages.error(request, 'Please select document type and upload a file.')
    
    context = {
        'kyc': kyc,
        'show_success_modal': show_success_modal
    }
    return render(request, 'verify.html', context)

@login_required(login_url='/login/')
def notifications(request):
    """Notifications page view"""
    from .models import Notification
    
    # Get user's notifications
    notifications = Notification.objects.filter(user=request.user)
    
    # Mark all as read when viewing the page
    unread_notifications = notifications.filter(is_read=False)
    for notification in unread_notifications:
        notification.mark_as_read()
        notification.save()
    
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required(login_url='/login/')
def support(request):
    """Support page view"""
    if request.method == 'POST':
        # Handle support ticket submission
        messages.success(request, 'Support ticket submitted successfully. We will respond within 24 hours.')
        return redirect('support')
    
    # In production, get user's actual tickets
    tickets = []
    return render(request, 'support.html', {'tickets': tickets})

def logout(request):
    """Logout view"""
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def swap(request):
    """Swap cryptocurrency page view"""
    if request.method == 'POST':
        # Handle swap submission
        messages.info(request, 'Swap processing initiated. Please contact support for assistance.')
        return redirect('swap')
    return render(request, 'swap.html')

@login_required
def link(request):
    """Link external wallet page view"""
    if request.method == 'POST':
        # Handle wallet linking
        messages.success(request, 'Wallet linking initiated. Please contact support for assistance.')
        return redirect('link')
    return render(request, 'link.html')

@login_required(login_url='/login/')
def order_card(request):
    """Order Web3 Card page view"""
    from django.conf import settings
    from .models import CardOrder
    
    if request.method == 'POST':
        # Handle card order submission
        try:
            xrp_amount = request.POST.get('xrp_amount')
            phone_number = request.POST.get('phone_number')
            full_address = request.POST.get('full_address')
            transaction_screenshot = request.FILES.get('transaction_screenshot')
            
            # Create card order
            card_order = CardOrder.objects.create(
                user=request.user,
                full_name=request.POST.get('full_name', f"{request.user.first_name} {request.user.last_name}"),
                email=request.POST.get('email', request.user.email),
                phone_number=phone_number,
                full_address=full_address,
                xrp_amount=xrp_amount,
                transaction_screenshot=transaction_screenshot
            )
            
            messages.success(request, 'Card order submitted successfully! You will be notified once processed.')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f'Error submitting order: {str(e)}')
            return redirect('order_card')
    
    context = {
        'xlm_address': settings.XLM_DEPOSIT_ADDRESS
    }
    return render(request, 'order_card.html', context)
