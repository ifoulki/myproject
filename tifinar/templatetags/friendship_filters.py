from django import template

register = template.Library()

@register.filter
def friendship_status_arabic(status):
    status_map = {
        'friends': 'أصدقاء',
        'request_sent': 'طلب مرسل', 
        'request_received': 'طلب مستلم',
        'not_friends': 'غير أصدقاء'
    }
    return status_map.get(status, status)

@register.filter
def friendship_status_icon(status):
    icon_map = {
        'friends': 'fas fa-user-friends text-success',
        'request_sent': 'fas fa-hourglass-half text-warning',
        'request_received': 'fas fa-bell text-info',
        'not_friends': 'fas fa-user-plus text-primary'
    }
    return icon_map.get(status, 'fas fa-user')