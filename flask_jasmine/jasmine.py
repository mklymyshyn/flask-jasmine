from __future__ import absolute_import

import os

from jinja2 import Environment, PackageLoader
from flask import Blueprint, send_from_directory


__all__ = ('Jasmine', 'Asset')

module = Blueprint('jasmine', __name__)


class Asset(object):
    def __init__(self, name):
        self.name = name

    def build(self, app):
        try:
            bundles = app.jinja_env.assets_environment._named_bundles
        except AttributeError:
            raise ImportError(u"Looks like Flask-Assets not initialized")

        try:
            contents = bundles.get(self.name).urls()
        except AttributeError:
            raise ValueError(
            u"Can't find `%s` Flask-Assets bundle" % self.name)

        return contents


class Jasmine(object):
    _static_dir = os.path.realpath(
        os.path.join(os.path.dirname(__file__), 'static'))
    _media_url = '/_jasmine/testrunner/media/'

    def __init__(self, app):
        self.app = app

        self.app.config.setdefault('JASMINE_SPECS', [])
        self.app.config.setdefault('JASMINE_SOURCES', [])

        if not app.debug:
            return

        self.jinja_env = Environment(
            autoescape=True,
            extensions=['jinja2.ext.i18n'],
            loader=PackageLoader('flask_jasmine', 'templates'))

        app.add_url_rule('%s<path:filename>' % self._media_url,
            '_jasmine.static', self.send_static_file)

        app.add_url_rule('/jasmine/testrunner/',
            '_jasmine.runner', self.runner_view)

        app.register_blueprint(module,
            url_prefix=self._media_url)

    def specs(self, *args):
        self.app.config['JASMINE_SPECS'].extend(list(args))

    def sources(self, *args):
        self.app.config['JASMINE_SOURCES'].extend(list(args))

    def build_sources(self, data):
        """
        Build list of sources from plain configs or
        build assets
        """

        lst = []

        for item in data:
            if isinstance(item, (str, unicode)):
                lst.append("%s/%s" % (self.app.static_url_path, item))
                continue

            if isinstance(item, Asset):
                contents = item.build(self.app)
                for asset_item in contents:
                    lst.append(asset_item)

        return lst

    def runner_view(self):
        """
        Render runner view
        """

        template_name = "runner.html"
        template = self.jinja_env.get_template(template_name)

        return template.render({
            'specs': self.build_sources(self.app.config['JASMINE_SPECS']),
            'sources': self.build_sources(self.app.config['JASMINE_SOURCES']),
            'media_url': self._media_url
        })

    def send_static_file(self, filename):
        """
        Send a static file from the flask-jasmine static directory
        """
        return send_from_directory(self._static_dir, filename)
