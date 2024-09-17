from setuptools import setup, find_packages

setup(
    name="download_pbi_xmla",
    version="0.4.2",  # Ensure this matches the version in pyproject.toml
    description="A package to fetch and save Power BI tables via XMLA endpoint",
    author="Danny Bharat",
    author_email="dannybharat@arkimetrix.com",
    url="https://github.com/DBArkimetrix/download_pbi_xmla",  # Example URL
    packages=find_packages(),  # Automatically find packages in the project
    install_requires=[
        "pythonnet>=3.0.3",
        "pyarrow>=16.1.0",
        "msal>=1.29.0",
        "python-dotenv>=1.0.1",
        "pandas>=2.2.2"
    ],
    python_requires=">=3.9,<4.0",  # Specify the compatible Python versions
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
