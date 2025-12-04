from setuptools import setup, find_packages

setup(
    name="ChatterBot",
    version="1.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "mathparse>=0.1,<0.3",
        "python-dateutil>=2.8,<2.11",
        "sqlalchemy>=2.0,<2.1",
        "spacy>=3.7.2,<3.9",
        "tqdm",
    ]
)
