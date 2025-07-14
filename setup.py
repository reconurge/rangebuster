from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Add test dependencies
test_requirements = [
    "pytest>=6.0",
    "pytest-cov>=2.0",
    "pytest-mock>=3.0",
]

setup(
    name="rangebuster",
    version="1.0.0",
    author="reconurge",
    description="A tool to search CIDRs based on keywords using RIR databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/reconurge/rangebuster",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: Security",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "test": test_requirements,
    },
    entry_points={
        "console_scripts": [
            "rangebuster=cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    test_suite="tests.run_tests",
) 