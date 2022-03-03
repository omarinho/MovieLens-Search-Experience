from setuptools import setup

version = "0.1"

setup(
    name='app',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    version=version,
    description="challenge",
)