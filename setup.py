from setuptools import find_packages, setup
from io import open

readme = open('README.md', encoding='utf-8').read()

setup(
    name='django-inventory-app',
    version='0.1',
    author='Sergey Panasenko',
    author_email='sergey.panasenko@gmail.com',
    description='Django inventory app',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[],
    include_package_data=True,
    license='AGPLv3+',
    url='https://github.com/sergey-panasenko/django-inventory-app',
    install_requires=[
        'Django>=2.2.6',
        'PyQRCode>=1.2.1',
        'reportlab>=3.5.31',
        'svglib>=0.9.2',
    ],
)
