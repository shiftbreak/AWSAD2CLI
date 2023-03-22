from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(

    name="awsad2cli",
    version="0.0.7",
    description="A tool to login to AWS via MS AAD SAML or AWS console using awsapps.com/console "
                "and assume a CLI role with support for MFA",
    url="https://github.com/shiftbreak/AWSAD2CLI",
    author="ShiftBreak",
    author_email="shiftbreak@password1.net",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="iam, boto, aws",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8, <4",
    install_requires=[
        "selenium",
        "configparser",
        "webdriver_manager",
        "argparse",
        "keyring",
        "selenium-wire",
        "boto3"
    ],
    entry_points={
        "console_scripts": [
            "awsad2cli=awsad2cli:main",
        ],
    },
)
