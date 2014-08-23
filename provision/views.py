from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .tasks import provision


@login_required
def home(request):
    return redirect(reverse('provision_inventory'))


@login_required
def inventory(request):
    return render(request, 'provision/inventory.html')


@login_required
def play(request):
    config = {
        'repo': 'https://github.com/mekanix/one-love-wordpress.git',
        'inventory': 'test',
        'playbook': 'site.yml',
        'remote_pass': 'vagrant',
    }
    provision.delay(config)
    return render(request, 'provision/play.html')
