"""
Simple setup configuration for the iTensorPy package.
"""

from setuptools import setup, find_packages

setup(
    name="itensorpy",
    version="0.2.5",
    author="iTensorPy Team",
    author_email="claudiuswebdesign@gmail.com",
    description="A Python package for tensor calculations in general relativity",
    url="https://github.com/Klaudiusz321/itensorpy",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "sympy>=1.7.1",
        "numpy>=1.19.0",
    ],
) 