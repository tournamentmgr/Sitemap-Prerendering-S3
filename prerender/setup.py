from setuptools import setup, find_packages
setup(
    name='prerender',
    version='1.5',
    description='A module to prerender webpages and post to S3',
    author='Dan Quackenbush',
    author_email='dan@tournamentmgr.com',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'requests',
        'urllib3',
        'xmltodict'
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