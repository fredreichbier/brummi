from setuptools import setup, find_packages
import sys, os

setup(name='brummi',
    version='0.1',
    description='ooc documentation generator',
    packages=['brummi'],
    include_package_data=True,
    package_data = {
        'brummi': ['templates/*.*'],
        },
    zip_safe=False,
    entry_points="""
    [console_scripts]
    brummi = brummi.main:run_brummi
    """,
    install_requires=[
        'jinja2',
        'markdown2',
        'pyooc',
    ]
)


