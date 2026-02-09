"""
Context processors to add global variables to all templates
"""

def dashboard_context(request):
    """
    Add dashboard-specific context variables
    """
    context = {}
    
    if request.user.is_authenticated:
        from .models import Notification
        
        # Get unread notifications count
        unread_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        
        context['unread_notifications_count'] = unread_count
    
    return context
