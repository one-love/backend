from django.shortcuts import render

from .tasks import provision

def home(request):
    config = {
        'repo': 'https://github.com/mekanix/one-love-wordpress.git',
        'inventory': 'test',
        'playbook': 'site.yml',
        'remote_pass': 'vagrant',
    }
    provision.delay(config)
    return render(request, 'provision/home.html')
