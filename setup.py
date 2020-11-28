import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='minimus',
    version='1.0',
    author='Igor Zyktin',
    author_email='nicord@yandex.ru',
    description='Small tool aiming to help making notes. '
                'Works with Markdown format and allows you '
                'to build cute graphs.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/IgorZyktin/minimus',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
