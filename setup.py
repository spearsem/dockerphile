from setuptools import setup, find_packages


setup(
    name='dockerphile',
    version='0.0.0',
    packages=find_packages(),
    install_requires = [
        'dockerfile==1.0.0'
    ],
)
