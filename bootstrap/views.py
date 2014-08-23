from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

from emailauth.auth import logout_if_loged_in


def home(request):
    context = RequestContext(request)
    next = '/'
    if request.method == 'POST':
        user_form = AuthenticationForm(data=request.POST)
        if user_form.is_valid():
            user = authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password'],
            )
            if user is not None:
                if user.is_active:
                    if 'next' in request.POST:
                        next = request.POST['next']
                    login(request, user)
                    return redirect(next)
    else:
        if request.user.is_authenticated():
            return redirect(reverse('provision_inventory'))
        if 'next' in request.GET:
            next = request.GET['next']

        user_form = AuthenticationForm()

    return render_to_response(
        'bootstrap/home.html',
        {
            'user_form': user_form,
            'next': next,
        },
        context,
    )


def logout(request):
    if request.user.is_authenticated():
        django_logout(request)
    return redirect('/')
