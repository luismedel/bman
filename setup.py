from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def main():
    setup(
        name="bman",
        version="0.9",
        description="Your command line bookmark manager.",
        long_description=read("README.md"),
        long_description_content_type="text/markdown",
        keywords="bookmarks",
        author="Luis Medel",
        author_email="luis@luismedel.com",
        url="https://github.com/luismedel/bman",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Intended Audience :: End Users/Desktop",
            "Operating System :: Unix",
            "Topic :: Internet",
            "Topic :: Database",
            "Topic :: Internet :: WWW/HTTP",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        ],
        package_dir={"": "src"},
        packages=find_packages("src"),
        include_package_data=True,
        install_requires=["click", "orjson"],
        entry_points={
            "console_scripts": [
                "bman=bman.main:bman",
            ],
        },
    )


if __name__ == "__main__":
    main()
