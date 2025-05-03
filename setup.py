#!/usr/bin/env python3
"""
Setup script for the Instagram Automation Tool package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="instagram-automation-tool",
    version="0.1.0",
    author="Your Organization",
    author_email="email@example.com",
    description="A comprehensive solution for automating Instagram account management, messaging, and content posting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/instagram-automation-tool",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.28.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "selenium>=4.10.0",
        "webdriver-manager>=4.0.0",
        "tqdm>=4.65.0",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "instagram-automation=run_improved:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.md"],
    },
)