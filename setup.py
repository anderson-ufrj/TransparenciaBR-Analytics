from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="transparenciabr-analytics",
    version="0.1.0",
    author="Anderson Henrique & Gianlucca",
    author_email="anderson.henrique@example.com",
    description="Análise avançada de dados do Portal da Transparência brasileiro",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anderson-ufrj/TransparenciaBR-Analytics",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "black>=23.12.0",
            "isort>=5.13.0",
            "flake8>=7.0.0",
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "transparencia-download=scripts.download_data:main",
            "transparencia-analyze=scripts.run_analysis:main",
            "transparencia-dashboard=scripts.deploy_streamlit:main",
        ],
    },
)