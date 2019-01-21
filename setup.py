from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    LONG_DESCRIPTION = f.read()

with open("requirements.txt") as f:
    GLOBAL_REQUIREMENTS = f.read().split("\n")

with open("scraper/requirements.txt") as f:
    SCRAPER = f.read().split("\n")
    SCRAPER += GLOBAL_REQUIREMENTS

with open("prerender/requirements.txt") as f:
    PRERENDER = f.read().split("\n")
    PRERENDER += GLOBAL_REQUIREMENTS

setup(
    name='scraper',
    version='1.0',
    description='A module to render webpages',
    long_description=LONG_DESCRIPTION,
    author='Dan Quackenbush',
    author_email='dan@tournamentmgr.com',
    packages=find_packages(),
    install_requires=SCRAPER,
    python_requires='>=3.4',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)

setup(
    name='prerender',
    version='1.0',
    description='A module to prerender webpages and post to S3',
    long_description=LONG_DESCRIPTION,
    author='Dan Quackenbush',
    author_email='dan@tournamentmgr.com',
    packages=find_packages(),
    install_requires=PRERENDER,
    python_requires='>=3.4',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
