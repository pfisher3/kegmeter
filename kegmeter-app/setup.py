from setuptools import setup, find_packages

setup(
    name="kegmeter-app",
    description="Kegmeter libraries used by both the app and the webserver",
    version="0.1",
    author="OmniTI Computer Consulting, Inc.",
    author_email="hello@omniti.com",
    namespace_packages=["kegmeter"],
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "kegmeter-common >= 0.1",
        "ago >= 0.0.6",
        "pygobject >= 3.8.2",
        "pyserial >= 2.7",
        "requests >= 1.2.3",
        "simplejson >= 3.6.5",
        ],
    scripts=[
        "scripts/kegmeter_app.py",
        ],
    )