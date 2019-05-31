from setuptools import find_packages, setup


def readfile(name):
    with open(name) as f:
        return f.read()


readme = readfile("README.rst")
changes = readfile("CHANGES.rst")

requires = []

docs_require = ["Sphinx", "pylons-sphinx-themes"]

tests_require = ["pytest", "pytest-cov", "setuptools"]

setup(
    name="plaster",
    version="1.0",
    description="A loader interface around multiple config file formats.",
    long_description=readme + "\n\n" + changes,
    author="Michael Merickel",
    author_email="pylons-discuss@googlegroups.com",
    url="https://docs.pylonsproject.org/projects/plaster/en/latest/",
    packages=find_packages("src", exclude=["tests"]),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.4",
    install_requires=requires,
    extras_require={
        "docs": docs_require,
        "testing": tests_require,
        ':python_version<"3.8"': ["importlib_metadata"],
    },
    test_suite="tests",
    zip_safe=False,
    keywords="plaster pastedeploy ini config",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
