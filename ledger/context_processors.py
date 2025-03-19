from .models import JournalType

def topnav_context_processor(request):
    return {'journal_types': JournalType.objects.all()}