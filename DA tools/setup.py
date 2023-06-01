import os
from setuptools import find_packages
from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(here, 'requirements.txt'), 'r', encoding='utf-8') as f:
    requirements = f.read()

metadata = {
    'name': 'paylab_award_model',
    'version': 'v0.4',
    'author': ['Xun Yang', 'Nick Bosworth', 'Justin Lee', 'Frank Zhang', 'Jerry Wang'],
    'author_email': ['xun.yang@pwc.com'],
    'maintainer': 'Xun Yang',
    'maintainer_email': 'xun.yang@pwc.com',
    'url': 'https://github.pwc.com/wage-trust/diamond-award_modules',
    'description': 'paylab_award_model',
    'long_description': long_description,
    'classifiers': ['Development Status :: 0.4',
                    'Programming Language :: Python',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.10',
                    'Intended Audience :: Data/Analytics',
                    'Topic :: Award Modeling',
                    'Operating System :: OS Independent'],
    'install_requires': requirements,
    'packages': find_packages(),
    'include_package_data': True,
    'package_dir': {'paylab_award_model': 'paylab_award_model'},
}

setup(**metadata)
