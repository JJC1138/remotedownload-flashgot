import setuptools

setuptools.setup(
    name = 'remotedownload-flashgot',
    version = '1.0.0dev',
    packages = setuptools.find_packages(),
    entry_points = {'console_scripts': [
        'remotedownload-flashgot = remotedownloadflashgot.__main__:main',
    ]},
)
