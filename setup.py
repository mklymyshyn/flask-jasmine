"""
Flask-Jasmine
-------------

This is extension to execute BDD tests with Jasmine BDD Framework.
Also extension support for Bundles created by ``Flask-Assets``.
"""

from setuptools import setup


setup(
    name='Flask-Jasmine',
    version='1.2',
    url='https://github.com/joymax/flask-jasmine',
    license='BSD',
    author='Maksym Klymyshyn',
    author_email='klymyshyn@gmail.com',
    description='Execution of Jasmine JavaScript tests within Flask',
    long_description=__doc__,
    packages=['flask_jasmine'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
