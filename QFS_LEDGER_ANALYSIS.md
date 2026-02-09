# QFS Ledger Project Analysis

## Overview
The QFS Ledger project is a full-stack cryptocurrency wallet management system built with Next.js (frontend) and Django (backend). The application uses dark mode theming with a sophisticated color palette and provides comprehensive user account management, KYC verification, deposit/receive functionality, and support ticketing system.

---

## Color Scheme & Design System

### Primary Colors
- **Primary**: `#99E39E` (Light Green) - Used for CTAs, buttons, highlights
- **Secondary**: `#1DC8CD` (Cyan/Teal)
- **Darkmode**: `#000510` (Very Dark Blue/Black) - Main background
- **Section**: `#737373` (Gray) - For section backgrounds with opacity
- **Muted**: `#d8dbdb` (Light Gray) - For secondary text

### Status Colors
- **Success**: `#3cd278` (Green) - For confirmed/verified states
- **Warning**: `#F7931A` (Orange) - For pending states  
- **Error**: `#CF3127` (Red) - For rejected/failed states

### Design Philosophy
- Dark mode throughout with glass morphism effects
- Borders use `border-section border-opacity-20` for subtle separation
- Backgrounds use `bg-section bg-opacity-10` for cards
- Text hierarchy: White for primary, Muted for secondary
- Consistent rounded corners (`rounded-lg`, `rounded-xl`)

---

## Layout Structure

### UserLayout Component
The main layout wrapper for authenticated user pages with:

#### Top Navigation Bar
- Logo: "ANON" (white) + "CRYPT" (primary color)
- Right side: 
  - Admin Panel link (only for admin emails)
  - Bell icon with notification count badge (red circle with number)
  - Profile avatar circle with first letter initial

#### Bottom Navigation (Fixed Footer)
Five icon-based navigation items:
1. **Settings** (gear icon) → `/profile`
2. **Notifications** (bell icon) → `/notifications`
3. **Wallet** (credit card icon) → `/dashboard`
4. **Support** (question mark icon) → `/support`
5. **Logout** (logout arrow icon) → Logs out user

Footer styling: Semi-transparent with backdrop blur, fixed to bottom of screen

---

## Page Breakdown

### 1. Dashboard (`/dashboard`)

**Purpose**: Main overview page showing account stats and backend connection status

**Layout Structure**:
```
┌─────────────────────────────────────────────┐
│ ANONCRYPT Dashboard Header                  │
│ Advanced Financial Management System        │
├─────────────────────────────────────────────┤
│ Backend Connection Card (Green status)      │
│ - Status, Message, Version                  │
├─────────────────────────────────────────────┤
│ Quick Stats Grid (4 columns)                │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐        │
│ │Total │ │Trans-│ │Total │ │Net   │        │
│ │Accts │ │actns │ │Assets│ │Income│        │
│ └──────┘ └──────┘ └──────┘ └──────┘        │
├─────────────────────────────────────────────┤
│ Architecture Info Card                      │
│ - Backend (Django) info                     │
│ - Frontend (React) info                     │
└─────────────────────────────────────────────┘
```

**Key Features**:
- API health check on mount
- Loading spinner during data fetch
- Error state with connection troubleshooting
- Card-based layout with consistent spacing
- Stats use different colors: blue, green, purple, indigo

---

### 2. Profile Page (`/profile`)

**Purpose**: User account management and password change

**Layout Structure**: Two-column grid (lg:grid-cols-2)

#### Left Column - Basic Details Card
- Profile picture: Circle with first initial
- User information (read-only):
  - Full Name
  - Email Address
  - User ID
  - Account Status (Green "Active")
  - Verification Status with dynamic badge:
    - **Verified** (green with checkmark) - No button
    - **Pending** (yellow with clock) - Disabled "Pending" button
    - **Rejected** (red with X) - "Resubmit" button → `/verify`
    - **Not Verified** (red with warning) - "Verify Now" button → `/verify`

#### Right Column - Change Password Card
- Form fields:
  - Current Password
  - New Password
  - Confirm New Password
- Password requirements box (list of rules)
- Submit button (full width, primary color)
- Security tips box at bottom

**Form Validation**:
- Checks password match
- Minimum 6 characters
- Shows loading state during submission
- Uses toast notifications for feedback

---

### 3. Send Page (`/send`)

**Purpose**: Send cryptocurrency to wallet addresses

**Layout Structure**: Two-column grid

#### Left Column - Send Form Card
**Form Fields**:
1. **Send From** (Dropdown)
   - Options: BTC, ETH, XRP, XLM, USDT, BNB, BNB Tiger
2. **Amount (USD)** (Number input)
   - Step: 0.01
   - Placeholder: "0.00"
3. **Wallet Address** (Text input)
   - Placeholder: "Paste wallet here"
   - Help text about network and gas fees
4. **Proceed Button**
   - Disabled when form incomplete
   - Shows spinner during processing

**Validation**:
- All fields required
- Amount must be valid number > 0
- Wallet address minimum 20 characters
- Real-time error messages below fields

#### Right Column - Transaction History Card
- Table with columns:
  - Date | Type | Amount | ID | Status
- Status badges with color coding
- Empty state with icon when no transactions

#### Processing Modal
**Unique Feature**: Modal appears when form submitted and **stays open indefinitely**
- Continuous spinning animations (multiple circles)
- "Processing Transaction" text
- Loading bar animation that loops
- No completion logic - stays in processing state forever

---

### 4. Receive Page (`/receive`)

**Purpose**: Generate deposit address for receiving cryptocurrency

**Layout Structure**: Two-column grid (left column height: fit-content)

#### Left Column - Receive Form Card
**Form Fields**:
1. **Select Coin** (Dropdown)
   - Same crypto options as Send page
2. **Proceed Button**
   - Disabled until coin selected
   - Shows spinner during processing

**Flow**:
- Creates deposit transaction via API
- Fetches user's deposit history on mount
- After successful creation, redirects to `/receive/details?coin={selectedCoin}`

#### Right Column - Transaction History Card
- **Limited to 10 most recent transactions**
- Scrollable with max height
- Table columns: Date | Coin | Amount | ID | Status
- Status badges: Confirmed (green), Pending (yellow), Rejected (red)
- Fetches real-time data from `/deposits/` API endpoint

#### Processing Modal
Same continuous loading modal as Send page

---

### 5. Notifications Page (`/notifications`)

**Purpose**: Display system notifications for user

**Page Header**:
- Title: "Notifications"
- Filter tabs: All | Unread | Support

**Features**:
- Fetches notifications from `/notifications/` API
- Fallback to mock data if API fails
- Each notification card shows:
  - Icon based on type (bell, ticket, checkmark, info)
  - Title and message
  - Timestamp (formatted as time ago)
  - Unread indicator (blue dot)
  - Action buttons for support-related notifications

**Notification Types**:
- `support_ticket` - Support ticket submitted
- `support_reply` - Admin response to ticket
- `kyc_update` - KYC status changes
- `general` - General announcements
- `system` - System messages

**Interaction**:
- Click notification to mark as read
- "Mark all as read" button
- Support notifications link to ticket details
- Graceful degradation if API fails

---

### 6. Support Page (Not fully shown but referenced)

**Purpose**: Submit and view support tickets

**Features**:
- Create new support tickets
- View ticket history
- Chat-style ticket responses
- Department categorization
- Priority levels

---

## Django Backend Models

### Key Models to Replicate:

#### 1. **KYCVerification**
```python
- user (OneToOne → User)
- status: not_submitted, pending, verified, rejected
- document_type: passport, drivers_license, national_id, etc.
- document_file (FileField)
- admin_notes
- submitted_at, reviewed_at, reviewed_by
```

#### 2. **SupportTicket**
```python
- ticket_id (ST-XXXXX format, auto-generated)
- user (ForeignKey)
- department: technical, billing, account, kyc, trading, general
- subject, message
- status: open, in_progress, waiting_for_user, closed
- priority: low, medium, high, urgent
- assigned_to (admin user)
- timestamps
```

#### 3. **SupportReply**
```python
- ticket (ForeignKey)
- user (can be customer or admin)
- message
- is_internal (for admin notes)
- created_at
```

#### 4. **Notification**
```python
- user (ForeignKey)
- type: support_ticket, support_reply, kyc_update, deposit_confirmed, etc.
- title, message
- is_read (Boolean)
- support_ticket (ForeignKey, nullable)
- created_at, read_at
- Method: mark_as_read()
```

#### 5. **DepositTransaction**
```python
- user (ForeignKey)
- coin_type: bitcoin, ethereum, ripple, stellar, usdt, bnb, bnb_tiger
- amount (Decimal, nullable)
- wallet_address (CharField 255)
- status: pending, confirmed, rejected
- admin_notes
- email_sent (Boolean)
- created_at, confirmed_at, processed_by
```

#### 6. **Wallet**
```python
- user (OneToOne)
- bitcoin_balance, ethereum_balance, ripple_balance, etc.
  (All stored as USD equivalent with 2 decimal places)
- Methods:
  - get_balance(coin_type)
  - add_balance(coin_type, amount)
  - subtract_balance(coin_type, amount)
```

#### 7. **WalletCopyTracking**
```python
- user (ForeignKey)
- coin_type
- (Tracks when users copy wallet addresses)
```

---

## Key UI Patterns

### Card Component Pattern
```jsx
<div className="bg-section bg-opacity-10 border border-section border-opacity-20 rounded-lg p-6">
  <h2 className="text-xl font-semibold text-white mb-6">Card Title</h2>
  {/* Content */}
</div>
```

### Form Input Pattern
```jsx
<div>
  <label className="block text-white font-medium mb-3">Label</label>
  <input
    className="w-full bg-darkmode border border-section border-opacity-30 focus:border-primary rounded-lg px-4 py-3 text-white focus:outline-none transition-colors"
    placeholder="Placeholder text"
  />
</div>
```

### Primary Button Pattern
```jsx
<button className="w-full bg-primary text-darkmode font-medium py-3 rounded-lg hover:bg-opacity-80 transition-colors disabled:opacity-50">
  Button Text
</button>
```

### Status Badge Pattern
```jsx
<span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border bg-green-500 bg-opacity-10 border-green-500 border-opacity-30 text-green-400">
  Verified
</span>
```

### Loading Spinner Pattern
```jsx
<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
```

### Processing Modal Pattern
```jsx
<div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
  <div className="bg-darkmode border border-section border-opacity-30 rounded-xl p-8 mx-4 max-w-sm w-full text-center">
    {/* Multiple spinning circles */}
    {/* Progress bar with infinite animation */}
    {/* Processing text */}
  </div>
</div>
```

---

## Authentication Flow

### Protected Routes
All user pages require authentication:
- Check `authService.isAuthenticated()` on mount
- Redirect to `/` (home) if not authenticated
- Fetch user profile data
- Show loading state while checking

### Logout Functionality
- Call `authService.logout()`
- Clear tokens from localStorage
- Show success toast
- Redirect to home page

---

## API Integration Patterns

### Authenticated Requests
```javascript
const token = localStorage.getItem('access_token');

const response = await fetch(`${API_BASE_URL}/endpoint/`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data),
});
```

### Error Handling
- Try-catch blocks for all API calls
- Fallback to mock data if API fails
- Show error toasts for user feedback
- Log errors to console for debugging
- Graceful degradation (don't break UI)

---

## Implementation Checklist for Web3 Project

### Phase 1: Color Scheme & Layout Setup
- [ ] Update Tailwind config with QFS color palette
- [ ] Create base layout component with top nav and bottom nav
- [ ] Implement dark mode theming
- [ ] Create reusable card component
- [ ] Create form input components
- [ ] Create button variants (primary, secondary, disabled)

### Phase 2: Django Models
- [ ] Create KYCVerification model
- [ ] Create SupportTicket model
- [ ] Create SupportReply model
- [ ] Create Notification model
- [ ] Create DepositTransaction model
- [ ] Create Wallet model
- [ ] Create WalletCopyTracking model
- [ ] Run migrations

### Phase 3: Dashboard Page
- [ ] Create dashboard template matching QFS layout
- [ ] Add backend connection status card
- [ ] Add quick stats grid (4 columns)
- [ ] Add architecture info card
- [ ] Implement loading and error states

### Phase 4: Profile Page
- [ ] Create two-column profile layout
- [ ] Add user details card (left)
- [ ] Add password change form (right)
- [ ] Implement KYC status display with dynamic badges
- [ ] Add verification redirect buttons
- [ ] Form validation and submission

### Phase 5: Send Page
- [ ] Create send form with 3 fields
- [ ] Add cryptocurrency dropdown
- [ ] Add amount and wallet address inputs
- [ ] Implement form validation
- [ ] Create transaction history table
- [ ] Add processing modal (infinite loop)

### Phase 6: Receive Page
- [ ] Create receive form with coin selector
- [ ] Implement deposit transaction creation
- [ ] Add transaction history (limited to 10)
- [ ] Add processing modal
- [ ] Redirect to details page after creation

### Phase 7: Notifications Page
- [ ] Create notifications list view
- [ ] Add filter tabs (All, Unread, Support)
- [ ] Implement notification type icons
- [ ] Add mark as read functionality
- [ ] Add mark all as read button
- [ ] Link support notifications to tickets

### Phase 8: API Endpoints
- [ ] Dashboard stats endpoint
- [ ] Profile update endpoint
- [ ] Password change endpoint
- [ ] KYC status endpoint
- [ ] Deposit creation endpoint
- [ ] Deposits list endpoint
- [ ] Notifications list endpoint
- [ ] Mark notification read endpoint

### Phase 9: Polish & Testing
- [ ] Responsive design testing
- [ ] Loading states on all pages
- [ ] Error handling and fallbacks
- [ ] Toast notifications
- [ ] Form validation messages
- [ ] Status badge styling
- [ ] Icon implementations

---

## Notes for Implementation

1. **Use existing authentication system**: Your current Django auth is good, just extend User model with profile fields

2. **Keep the color scheme exactly**: 
   - Primary: `#99E39E` (not your current `#F65B1A` orange)
   - Update all buttons and CTAs to use this green

3. **Processing modal behavior**: The send/receive processing modals are designed to **never complete** - they loop indefinitely (this is intentional, likely for admin manual processing)

4. **Transaction tables**: Always show most recent first, limit receive page to 10 items

5. **KYC integration**: The profile page prominently features KYC status - make this a core feature

6. **Bottom navigation is critical**: Fixed footer with 5 icons is the primary navigation method on mobile

7. **Notifications are real-time**: Connect to backend, but gracefully fallback to mock data

8. **All cards follow same pattern**: `bg-section bg-opacity-10` with `border-section border-opacity-20`

9. **Text hierarchy**:
   - Headers: `text-white text-2xl font-bold`
   - Labels: `text-white font-medium`
   - Body: `text-white`
   - Secondary: `text-muted`

10. **Empty states**: All lists/tables have nice empty state with icon and message
