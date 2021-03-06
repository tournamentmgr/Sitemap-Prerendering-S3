from setuptools import setup, find_packages
setup(
    name='scraper',
    version='1.5',
    description='A module to render webpages',
    author='Dan Quackenbush',
    author_email='dan@tournamentmgr.com',
    packages=find_packages(),
    install_requires=[
        'pyppeteer==0.2.2'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
