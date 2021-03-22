from setuptools import setup, find_packages

setup(
    name='colorize',
    description='Colorization app for manga',

    author='Vitaly Sopov',
    author_email='vvsopov@edu.hse.ru',

    packages=find_packages(),

    include_package_data=True,
    install_requires=['numpy', 'PyQt5', 'qimage2ndarray', 'shapely'],
    entry_points={
        'console_scripts': [
            'colorize = colorize.main:main',
        ],
    },
)