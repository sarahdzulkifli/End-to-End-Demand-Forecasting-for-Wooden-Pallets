from setuptools import setup, find_packages
import pathlib

# Read requirements from requirements.txt
here = pathlib.Path(__file__).parent.resolve()
requirements = []
if (here / "requirements.txt").exists():
    with open(here / "requirements.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("-r"):
                requirements.append(line)

setup(
    name="demand-forecasting",
    version="1.0.0",
    author="Sarah Dzulkifli",
    author_email="sarahdzulkifli@gmail.com",
    description="Wooden pallet demand forecasting system",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.11,<3.13",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
    ],
)