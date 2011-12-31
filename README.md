# Flask-Jasmine

Extension to execute **[Jasmine](http://pivotal.github.com/jasmine/)** JavaScript Tests. At the moment it's a bit annoying to integrate Jasmine within well organized JS sources using **[Flask-Assets](http://flask-assets.readthedocs.org/en/latest/index.html)**

**Flask-Jasmine** work only in **debug** mode of the App.

## Installation

Install the extension with one of the following commands:

	easy_install Flask-Jasmine

or alternatively if you have pip installed:
	
	pip install Flask-Jasmine


## Usage

You initialize app by creating Jasmine instance and set specs and sources of your JavaScript:

	from flask import Flask
	from flask.ext.jasmine import Jasmine

	app = Flask('sample_app')

	jasmine = Jasmine(app)

    jasmine.specs(
        'src/specs/spec1.js',
        'src/specs/spec2.js',
    )

    jasmine.sources(
        'src/js/file1.js'
        'src/js/file2.js'
    )

### With Flask-Assets

To using **Flask-Jasmine** with **Flask-Assets** you need to create instance of `Asset` 
with name of appropriate `Bundle`. At the moment unnamed bundles are not supported.

	from flask import Flask
	from flask.ext.jasmine import Jasmine, Asset
	from flaskext.assets import Environment, Bundle

	app = Flask('sample_app')

	assets = Environment(app)	
	bundle1 = Bundle(
		'src/libs/jquery.cookie.js',
		'src/libs/jquery.tmpl.js',	
		output='utils.js',
		filters='yui_js'
	)
	assets.register('utils', bundle1)

	jasmine = Jasmine(app)
    jasmine.specs(
        'src/specs/spec1.js',
        'src/specs/spec2.js',
    )
    jasmine.sources(
        Asset('utils')
    )


## Start tests

To start tests go to `http://127.0.0.1:5000/jasmine/testrunner/`
