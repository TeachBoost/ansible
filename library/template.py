from os import path

from bottle import SimpleTemplate

import settings


class Template(object):
    templates = {}

    def __init__(self):
        self.context = {
            '_template_dir': settings.TEMPLATE_DIR,
            '_static_path': settings.STATIC_PATH,
            '_basepath': settings.BASEPATH,
            '_public_url': settings.PUBLIC_URL,
        }

    def render(self, name, **vars):
        template = self.templates.get(name, self.load(name))
        if name not in self.templates and not settings.DEBUG:
            self.templates[name] = template
        vars.update(self.context)
        return template.render(vars)

    def load(self, name):
        filename = path.join(settings.TEMPLATE_DIR, name)
        handle = open(filename)
        data = handle.read()
        handle.close()
        return SimpleTemplate(data)
