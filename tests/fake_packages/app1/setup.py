from setuptools import setup, find_packages

setup(
    name="app1",
    version="1.0",
    packages=find_packages(),
    entry_points={
        'plaster.loader_factory': [
            'conf=app1.loaders:ConfLoader',
            'ini=app1.loaders:INILoader',
            'yaml=app1.loaders:YAMLLoader',
            'yaml+foo=app1.loaders:YAMLFooLoader',
            'dup=app1.loaders:DuplicateLoader',
            'bad=app1.loaders:BadLoader',
            'broken=app1.loaders.BadLoader',
        ],
        'plaster.loader_factory.wsgi': [
            'ini=app1.loaders:INIWSGILoader',
        ],
        'other.loader': [
            'ini=app1.loaders:WontBeLoaded',
        ],
    },
)
