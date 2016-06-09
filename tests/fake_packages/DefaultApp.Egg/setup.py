from setuptools import setup, find_packages

setup(
    name="DefaultApp",
    version="1.0",
    packages=find_packages(),
    entry_points={
        'plaster.loader': """
            ini=defaultapp.loaders:INILoader
            ini+other=defaultapp.loaders.INIOtherLoader
            yaml=defaultapp.loaders:YAMLLoader
            yaml+other=defaultapp.loaders:YAMLOtherLoader
            bad=defaultapp.loaders.BadLoader
        """,
        'other.loader': """
            ini=defaultapp.loaders:WontBeLoaded
        """
    },
)
