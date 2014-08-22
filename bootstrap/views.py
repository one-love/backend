from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from .forms import UserForm


def home(request):
    context = RequestContext(request)
    if request.method == 'POST':
        if request.user.is_authenticated():
            logout(request)
            return redirect('/')
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = None
            try:
                user = get_user_model().objects.get(
                    email=user_form.cleaned_data['email']
                )
            except:
                pass
            if user is not None:
                user = authenticate(
                    username=user.username,
                    password=user_form.cleaned_data['password'],
                )
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('/')
    else:
        user_form = UserForm()

    return render_to_response(
        'bootstrap/home.html',
        {
            'user_form': user_form,
        },
        context,
    )
