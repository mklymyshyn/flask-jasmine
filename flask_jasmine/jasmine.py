from __future__ import absolute_import

import os

from jinja2 import Environment, PackageLoader
from flask import Blueprint, send_from_directory


__all__ = ('Jasmine', 'Asset', 'JasmineSpecfile')

module = Blueprint('jasmine', __name__)


class Asset(object):
    def __init__(self, name):
        self.name = name
        self.app = None

    @property
    def bundles(self):
        try:
            bundles = self.app.jinja_env.assets_environment._named_bundles
        except AttributeError:
            raise ImportError(u"Looks like Flask-Assets not initialized")

        return bundles

    def contents(self, app):
        """
        Here is direty hack to convert urls
        to absolute paths. Webassets aren't friendly
        enough to write proper code
        """
        self.app = app
        urls = self.build(app)
        rv = []
        for url in urls:
            rv.append("%s/%s" % (
                app.static_folder,
                url[len(app.config.get('ASSETS_URL')):]
            ))

        return rv

    def build(self, app):
        self.app = app
        try:
            contents = self.bundles.get(self.name).urls()
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


# In case Flask-Script available we
# define custom flask-script command to
# generate specrunner

# NB: this is shitty implementation/idea checking
# should be cleaned up
try:
    from flask.ext.script import Command

    class JasmineSpecfile(Command):
        """Command to generate SpecRunner for Jasmine
        """

        def run(self):
            from flask.ext import jasmine
            from jinja2 import Template
            import os

            # we need more elegant solution
            app = self.app

            # set ASSETS_DEBUG to True to
            # avoid compilation of source codes
            app.config['ASSETS_DEBUG'] = True

            sources = app.config.get('JASMINE_SOURCES', [])
            specs = [os.path.join(app.static_folder, fl) \
                        for fl in app.config.get('JASMINE_SPECS', [])]
            specs.extend(sources)

            lib_base = os.path.join(
                os.path.dirname(jasmine.__file__),
                'static',
                'jasmine'
            )
            lib_files = [os.path.join(lib_base, fl) for fl in (
                'jasmine.js',
                'jasmine-html.js',
                'contrib/jasmine.console_reporter.js',
                'contrib/jasmine.junit_reporter.js'
            )]

            files = []

            for source in specs:
                if isinstance(source, jasmine.Asset):
                    files.extend(source.contents(app))
                else:
                    files.extend([source])

            templates_path = os.path.join(
                os.path.dirname(jasmine.__file__),
                "templates"
            )

            template = Template(
                open(os.path.join(
                    templates_path,
                    "SpecRunner.html"
                )).read()
            )

            print template.render(files=files, jasmine=lib_files)

except ImportError:
    pass
