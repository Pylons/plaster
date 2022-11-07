from setuptools import find_packages, setup

setup(
    name="app1",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "plaster.loader_factory": [
            "conf=app1.loaders:ConfLoader",
            "file+conf=app1.loaders:ConfLoader",
            "ini=app1.loaders:INIWSGILoader",
            "file+ini=app1.loaders:INIWSGILoader",
            "file+yaml=app1.loaders:YAMLLoader",
            "yaml+foo=app1.loaders:YAMLFooLoader",
            "dup=app1.loaders:DuplicateLoader",
            "bad=app1.loaders:BadLoader",
            "broken=app1.loaders.BadLoader",
        ],
        "plaster.wsgi_loader_factory": [
            "ini=app1.loaders:INIWSGILoader",
            "file+ini=app1.loaders:INIWSGILoader",
        ],
        "plaster.dummy1_loader_factory": [
            "ini=app1.loaders:INIWSGILoader",
            "file+ini=app1.loaders:INIWSGILoader",
        ],
        "plaster.dummy2_loader_factory": [
            "ini=app1.loaders:INILoader",
            "file+ini=app1.loaders:INILoader",
        ],
        "other.loader": ["ini=app1.loaders:WontBeLoaded"],
    },
)
