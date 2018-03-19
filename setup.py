from setuptools import setup, find_packages

setup(
    name='IPBot Telegram',
    version='0.1',
    long_description=__doc__,
    py_modules=('ipbot',),
    install_requires=['DepyTG', 'requests'],
    dependency_links=[
        "https://github.com/Depau/DepyTG/archive/wip.zip"
    ],
    entry_points={
        'console_scripts': [
            'ipbot = ipbot:main',
        ]
    }
)
