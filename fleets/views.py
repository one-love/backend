from django.views.generic import CreateView

from fleets.models import Fleet


class FleetCreateView(CreateView):
    template_name = 'fleets/create.html'
    model = Fleet
