# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

from setuptools import setup, find_packages

setup(
    name="aegis-elite",
    version="12.0.0",
    author="Wahyu Nur Iman",
    description="AEGIS Elite — Enterprise AI Engineering Cognitive Runtime Platform",
    long_description=open("README.md").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/wahyunuriman999/AEGIS-ELITE",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "pyyaml>=6.0",
    ],
    extras_require={
        "studio": [],  # No extra deps - uses stdlib http.server
    },
    entry_points={
        "console_scripts": [
            "aegis=aegis:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    keywords="ai engineering governance code-review architecture-analysis cognitive-runtime",
)
