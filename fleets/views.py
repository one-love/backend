from django.views.generic import CreateView

from fleets.models import Fleet


class FleetCreate(CreateView):
    template_name = 'fleets/create.html'
    model = Fleet
    fields = ['name', 'url']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(FleetCreate, self).form_valid(form)
