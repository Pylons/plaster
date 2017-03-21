=======
plaster
=======

.. image:: https://img.shields.io/pypi/v/plaster.svg
    :target: https://pypi.python.org/pypi/plaster

.. image:: https://img.shields.io/travis/mmerickel/plaster.svg
    :target: https://travis-ci.org/mmerickel/plaster

.. image:: https://readthedocs.org/projects/plaster/badge/?version=latest
    :target: https://readthedocs.org/projects/plaster/?badge=latest
    :alt: Documentation Status

``plaster`` is a loader interface around multiple config file formats. It
exists to define a common API for applications to use when they wish to load
configuration. The library itself does not aim to handle anything except
a basic API that applications may use to find and load configuration settings.
Any specific constraints should be implemented in a pluggable loader which can
be registered via an entrypoint.

See http://plaster.readthedocs.io/ or ``docs/index.rst`` in this distribution
for detailed documentation.
