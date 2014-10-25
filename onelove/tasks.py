from __future__ import absolute_import

import os
import subprocess

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


