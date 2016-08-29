import setuptools

setuptools.setup(
    name = 'remotedownload',
    version = '1.0.0dev',
    packages = setuptools.find_packages(),
    entry_points = {'console_scripts': [
        'remotedownloadsend = remotedownload.send:main',
        'remotedownloadget = remotedownload.get:main',
    ]},
    install_requires = ['requests'],
)
