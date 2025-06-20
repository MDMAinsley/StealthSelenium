from setuptools import setup, find_packages

setup(
    name='stealth_selenium',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'undetected-chromedriver',
        'selenium',
    ],
    author='Your Name',
    description='Undetectable Selenium wrapper with real browser behavior',
    url='https://github.com/YOUR_USER/stealth_selenium',
)
