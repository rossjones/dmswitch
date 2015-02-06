try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


setup(
    name='dmswitch',
    version="0.0.1",
    author='Ross Jones',
    author_email='ross@servercode.co.uk',
    license="MIT",
    url='http://github.com/rossjones/dmswitch/',
    description="Complains when the switch hasn't been switched",
    zip_safe=False,
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['dmswitch', 'dmswitch.bin'],
    include_package_data=True,
    dependency_links=[
        "http://github.com/davidmiller/ffs/tarball/master#egg=ffs-0.0.8",
    ],
    install_requires = [
        "ffs==0.0.8"
    ],
    entry_points = {
        'console_scripts': [
            'dmswitch=dmswitch.bin.cli:main',
        ],
    }
)