"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='prometheus_cms',
    version='0.1.0',
    description='Prometheus Content management system',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/face-digital/prometheus_cms',
    author='FACE Digital',
    author_email='wizzzet@gmail.com',
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='cms content management system',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['django>=2.0', 'django-modeltranslation', 'django-solo', 'Pillow'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    project_urls={
        'Bug Reports': 'https://github.com/face-digital/prometheus_cms/issues',
        'Source': 'https://github.com/face-digital/prometheus_cms',
    },
)