from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='scraper',
    version='1.2',
    description='A module to render webpages',
    long_description=LONG_DESCRIPTION,
    author='Dan Quackenbush',
    author_email='dan@tournamentmgr.com',
    packages=find_packages(),
    install_requires=[
        'pyppeteer'
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

setup(
    name='prerender',
    version='1.2',
    description='A module to prerender webpages and post to S3',
    long_description=LONG_DESCRIPTION,
    author='Dan Quackenbush',
    author_email='dan@tournamentmgr.com',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'requests'
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
