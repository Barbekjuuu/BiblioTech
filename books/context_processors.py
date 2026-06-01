from .models import Powiadomienie


def unread_notifications(request):
    if request.user.is_authenticated:
        return {
            'unread_notifications_count': request.user.powiadomienia.filter(przeczytane=False).count()
        }
    return {}
