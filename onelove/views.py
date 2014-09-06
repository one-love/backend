import json

from django.contrib.auth import login, logout as django_logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView

from .documents import Fleet


class HomeView(FormView):
    template_name = 'onelove/index.html'
    form_class = AuthenticationForm
    success_url = '/'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        if self.request.user.is_authenticated():
            context['fleet_list'] = Fleet.objects.filter(
                user=self.request.user
            )
        return context

    def form_valid(self, form):
        if form.data['next']:
            self.success_url = form.data['next']
        login(self.request, form.get_user())
        return super(HomeView, self).form_valid(form)

    def JsonResponse(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(HomeView, self).form_invalid(form)
        if self.request.is_ajax():
            return self.JsonResponse(form.errors, status=403)
        else:
            return response


def logout(request):
    if request.user.is_authenticated():
        django_logout(request)
    return redirect('/')
