from setuptools import setup

setup(
    name="wordlist",
    version="0.2.0",
    packages=["wordlist"],
    description="creates a list of words from various corpora",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mwartell/wordlist",
    author="matt wartell",
    author_email="matt.wartell@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.3",
    license="MIT",
    package_data={"wordlist": ["worddata/*"]},
    entry_points={"console_scripts": ["xkcd-pass = wordlist.xkcd_pass:main"]},
)
