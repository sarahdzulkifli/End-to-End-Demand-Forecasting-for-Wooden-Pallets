from setuptools import setup, find_packages

setup(
    name="demand-forecasting",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Wooden pallet demand forecasting system",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.103.1",
        "uvicorn[standard]>=0.23.2",
        "pandas>=2.1.0",
        "numpy>=1.24.3",
        "scikit-learn>=1.3.0",
        "xgboost>=2.0.0",
        "prophet>=1.1.5",
        "statsmodels>=0.14.0",
    ],
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
)