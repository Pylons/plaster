from setuptools import setup, find_packages

with open('README.rst') as fp:
    readme = fp.read()

with open('CHANGES.rst') as fp:
    changes = fp.read()

requires = [
    'setuptools', # for pkg_resources
]

docs_require = [
    'Sphinx',
]

tests_require = [
    'pytest',
]

setup(
    name='plaster',
    version='0.1.0',
    description="A loader interface around multiple config file formats.",
    long_description=readme + '\n\n' + changes,
    author="Michael Merickel",
    author_email='michael@merickel.org',
    url='https://github.com/mmerickel/plaster',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=requires,
    extras_require={
        'docs': docs_require,
        'testing': tests_require,
    },
    zip_safe=False,
    keywords='plaster pastedeploy ini config',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
