import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="transaction-scan",
    version="1.0.0",
    description="Scans CSV files exported from various institutions to save and analyse transactions.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/realpython/transactionscan",
    author="Dino Fizzotti",
    author_email="dino@dinofizzotti.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["transactionscan", "transactionscan.db", "transactionscan.models", "transactionscan.parsers"],
    include_package_data=True,
    install_requires=["sqlalchemy"],
    entry_points={
        "console_scripts": [
            "transaction-scan=transactionscan.__main__:main",
        ]
    },
)