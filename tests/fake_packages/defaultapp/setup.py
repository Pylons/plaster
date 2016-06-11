from setuptools import setup, find_packages

setup(
    name="DefaultApp",
    version="1.0",
    packages=find_packages(),
    entry_points={
        'plaster.loader': [
            'conf=defaultapp.loaders:ConfLoader',
            'ini+foo=defaultapp.loaders:INILoader',
            'yaml+foo=defaultapp.loaders:YAMLFooLoader',
            'yaml+bar=defaultapp.loaders:YAMLBarLoader',
            'bad=defaultapp.loaders:BadLoader',
            'broken=defaultapp.loaders.BadLoader',
        ],
        'other.loader': [
            'ini=defaultapp.loaders:WontBeLoaded',
        ],
    },
)
