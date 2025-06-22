from setuptools import setup, find_packages

setup(
    name='stealth_selenium',
    version='0.51',
    packages=find_packages(),
    install_requires=[
        'undetected-chromedriver',
        'selenium',
    ],
    author='MDMAinsley',
    description='Undetectable Selenium wrapper with real browser behavior',
    url='https://github.com/MDMAinsley/StealthSelenium.git',
)
