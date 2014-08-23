from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.contrib.auth.forms import AuthenticationForm


def home(request):
    context = RequestContext(request)
    if request.method == 'POST':
        if request.user.is_authenticated():
            logout(request)
            return redirect('/')
        user_form = AuthenticationForm(data=request.POST)
        if user_form.is_valid():
            user = authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password'],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
    else:
        user_form = AuthenticationForm()

    return render_to_response(
        'bootstrap/home.html',
        {
            'user_form': user_form,
        },
        context,
    )
