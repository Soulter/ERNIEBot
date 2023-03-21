from setuptools import find_namespace_packages
from setuptools import setup

setup(
    name="Wenxin",
    version="1.0",
    description="a reverse engineering of ERNIEBot",
    long_description=open("README.md", "rt", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Soulter/ERNIEBot",
    project_urls={
        "Bug Report": "https://github.com/Soulter/ERNIEBot/issues"
    },
    author="Soulter",
    author_email="905617992@qq.com",
    license="GNU Affero General Public License v3.0",
    packages=find_namespace_packages("src"),
    package_dir={"": "src"},
    py_modules=["wenxin"],
    package_data={"": ["*.json"]},
    install_requires=[
        "selenium==4.8.2",
        "browsermob-proxy==0.8.0",
        "requests"
    ],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: Chinese",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)