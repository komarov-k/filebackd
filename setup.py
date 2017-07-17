from setuptools import setup, find_packages

setup(
    name='filebackd',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'click',
        'watchdog'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ],
    entry_points='''
        [console_scripts]
        filebackd=filebackd.filebackd:cli
    '''
)
