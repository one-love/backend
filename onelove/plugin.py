import importlib


class Plugin(object):
    def __init__(self, provider=None, knowledge=None):
        self.provider = provider
        self.knowledge = knowledge


def load_hosting_providers(providers):
    result = {}
    for plugin_name in providers:
        plugin_module = importlib.import_module(plugin_name)
        plugin = plugin_module.plugin
        provider = plugin.provider
        if provider is None:
            print('provider %s is invalid' % plugin_name)
            break
        result[provider.type] = provider
    return result


def load_knowledge_sources(knowledges):
    result = {}
    for plugin_name in knowledges:
        plugin_module = importlib.import_module(plugin_name)
        plugin = plugin_module.plugin
        knowledge = plugin.knowledge
        if knowledge is None:
            print('provider %s is invalid' % plugin_name)
            break
        result[knowledge.type] = knowledge
    return result
