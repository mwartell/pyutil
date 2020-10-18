from setuptools import setup

setup(
    name="pyutil",
    version="0.1",
    packages=["pyutil"],
    license="MIT",
    long_description=open("README.md").read(),
    package_data={"pyutil": ["worddata/*"]},
    entry_points={"console_scripts": ["xkcd-pass = pyutil.xkcd_pass:main"]},
)
