from pmpmanager.__version__ import version
from sys import version_info

if version_info < (2, 6):
    import sys
    print "Please use a newer version of python"
    sys.exit(1)



try:
    from setuptools import setup, find_packages
except ImportError:
	try:
            from distutils.core import setup
	except ImportError:
            from ez_setup import use_setuptools
            use_setuptools()
            from setuptools import setup, find_packages

# we want this module for nosetests
try:
    import multiprocessing
except ImportError:
    # its not critical if this fails though.
    pass

setup(name='pmpman',
    version=version,
    description="pmpman uses udeve  to stream music to usb sitcks and media players",
    long_description="""pmpman uses udeve  to stream music to usb sitcks and media players""",
    author="O M Synge",
    author_email="osynge@suse.com",
    license='The MIT License (MIT)',
    url = 'https://github.com/hepix-virtualisation/pmpman',
    packages = ['pmpmanager', 'pmpmanager/db_jobs/', 'pmpmanager/jobs/'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Audio'
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        ],

    scripts=['pmpman_udev.sh','pmpman_cli'],
    data_files=[('share/doc/pmpman-%s' % (version),['README.md','LICENSE','ChangeLog','udev/rules.d/95-pmpman.rules'])],
    tests_require=[
        'coverage >= 3.0',
        'nose >= 1.1.0',
        'mock',
        'SQLAlchemy >= 0.7.8',
    ],
    setup_requires=[
        'nose',
        'SQLAlchemy >= 0.7.8',
    ],
    test_suite = 'nose.collector',
    )
