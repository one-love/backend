One Love WEB interface
======================

WEB part of [One Love project](https://github.com/one-love/one-love). Basicly, it sends JSON to [workers](https://github.com/one-love/workers) through RabbitMQ. Example of such JSON:

    {
        'repo': 'https://github.com/mekanix/one-love-wordpress.git',
        'inventory': 'provision/test',
        'playbook': 'provision/site.yml',
        'sudopass': 'secrit',
    }
