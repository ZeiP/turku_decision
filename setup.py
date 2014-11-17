from setuptools import setup, find_packages

setup(
    name='turku_decisions',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = turku_decisions.settings']},
)
