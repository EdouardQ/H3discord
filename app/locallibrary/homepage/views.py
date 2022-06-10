from django.http import HttpResponse
from django.template import loader

from .models import History


def index(request):
    logs = History.objects.all()
    template = loader.get_template('index.html')
    context = {
        'logs': logs,
    }
    return HttpResponse(template.render(context, request))


