import os
from setuptools import setup, find_packages

setup(
    name="kegmeter-web",
    description="Kegmeter web server",
    version="0.1",
    author="OmniTI Computer Consulting, Inc.",
    author_email="hello@omniti.com",
    license="MIT",
    namespace_packages=["kegmeter"],
    packages=find_packages(),
    install_requires=[
        "pysqlite >= 2.6.3",
        "tornado >= 4.0.2",
        ],
    scripts=[
        "scripts/kegmeter_web.py",
        ],
    )