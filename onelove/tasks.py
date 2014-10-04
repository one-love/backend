from __future__ import absolute_import

import os
import subprocess

import ansible
from ansible import inventory, playbook
from celery import shared_task


def repo_name(repo):
    if repo.endswith('.git'):
        repo = repo[:-4]
    repo_name = os.path.split(repo)[1]
    return repo_name


def clone_or_pull(repo_url):
    repo = repo_name(repo_url)
    if os.path.exists(repo):
        os.chdir(repo)
        command = 'git pull --rebase --recurse-submodules'
    else:
        command = 'git clone --recursive --depth=1 ' + repo_url
    process = subprocess.Popen(command.split(' '))
    process.wait()
    return process.returncode


def play(config):
    inventory_path = config['inventory']
    inv = inventory.Inventory(inventory_path)
    inv.set_playbook_basedir(os.path.dirname(inventory_path))
    stats = ansible.callbacks.AggregateStats()
    playbook_cb = ansible.callbacks.PlaybookCallbacks(
        verbose=ansible.utils.VERBOSITY,
    )
    runner_cb = ansible.callbacks.PlaybookRunnerCallbacks(
        stats,
        verbose=ansible.utils.VERBOSITY,
    )

    pb = playbook.PlayBook(
        playbook=config['playbook'],
        inventory=inv,
        callbacks=playbook_cb,
        runner_callbacks=runner_cb,
        stats=stats,
        remote_pass=config['remote_pass'],
    )

    return pb.run()


@shared_task
def provision(config):
    os.environ['HOME'] = '/tmp'
    os.chdir('/var/repos')
    clone_or_pull(config['repo'])
    os.chdir('/var/repos/' + repo_name(config['repo']))
    return play(config)
