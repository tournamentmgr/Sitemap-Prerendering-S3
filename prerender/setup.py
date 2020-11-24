from setuptools import setup, find_packages
setup(
    name='prerender',
    version='1.6',
    description='A module to prerender webpages and post to S3',
    author='Dan Quackenbush',
    author_email='dan@tournamentmgr.com',
    packages=find_packages(),
    install_requires=[
        'boto3==1.16.4',
        'requests==2.25.0',
        'urllib3==1.26.2',
        'xmltodict==0.12.0'
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
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
