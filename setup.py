import setuptools

from minimus import constants

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='minimus',
    version=constants.__version__,
    author='Igor Zyktin',
    author_email='nicord@yandex.ru',
    description='Small tool aiming to help making notes '
                'in Markdown format.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/IgorZyktin/minimus',
    packages=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
