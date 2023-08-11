import re
from typing import List

from setuptools import (
    find_packages,
    setup,
)


def read_file(file_path: str, encoding: str = 'utf-8') -> str:
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read()


def read_requirements(file_path: str, encoding: str = 'utf-8') -> List[str]:
    with open(file_path, 'r', encoding=encoding) as f:
        requires = [
            re.sub(r'(.*)#egg=(.*)', r'\2 @ \1', line.strip())  # replace #egg= with @
            for line in f
            if line.strip() and not line.startswith('#')  # ignore empty lines and comments
        ]
    return requires


long_description: str = read_file('README.md')
requires: List[str] = read_requirements('requirements.txt')

setup(
    name='ondewo-sip-client',
    version='5.1.0',
    author='Ondewo GbmH',
    author_email='office@ondewo.com',
    description='provides endpoints and messages for gRPC communication with the ONDEWO SIP server',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ondewo/ondewo-sip-client-python',
    packages=[
        np
        for np in filter(
            lambda n: n.startswith('ondewo.') or n == 'ondewo',
            find_packages()
        )
    ],
    include_package_data=True,
    package_data={
        'ondewo.sip': ['py.typed', '*.pyi'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=requires,
)
