from setuptools import setup, find_packages

setup(
    name="pyjst",
    version='0.1.0',
    packages=find_packages('.'),
    zip_safe = True,
    include_package_data = False,
    install_requires = [],
    entry_points = {
        'console_scripts':[
            'pyjst=pyjst:main',
        ]
    }
)
