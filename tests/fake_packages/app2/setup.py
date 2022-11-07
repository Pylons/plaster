from setuptools import find_packages, setup

setup(
    name="app2",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "plaster.loader_factory": [
            "dup=app2.loaders:DuplicateLoader",
            "yaml+bar=app2.loaders:YAMLBarLoader",
        ]
    },
)
