from django.views.generic import CreateView, DetailView, UpdateView
from django.core.urlresolvers import reverse

from fleets.models import Fleet


class FleetCreate(CreateView):
    model = Fleet
    fields = ['name', 'url']

    def get_success_url(self):
        url = reverse('fleet_detail', args=[self.object.slug])
        return url

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(FleetCreate, self).form_valid(form)


class FleetDetail(UpdateView):
    model = Fleet
    fields = ['name', 'url', 'hosting', 'app']
    template_name_suffix = '_detail'
