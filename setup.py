# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['newclear']

package_data = \
{'': ['*']}

install_requires = \
['click-skeleton>=0.15,<0.16',
 'defopt>=6.0.1,<7.0.0',
 'makefun>=1.9.3,<2.0.0',
 'returns>=0.16.0,<0.17.0']

entry_points = \
{'console_scripts': ['newclear = newclear.main:main']}

setup_kwargs = {
    'name': 'newclear',
    'version': '0.1.0',
    'description': 'New style CLI builder',
    'long_description': None,
    'author': 'Adrien Pensart',
    'author_email': 'crunchengine@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)

