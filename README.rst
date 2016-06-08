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
a basic API for applications to depend on. Any specific constraints should
be implemented in a pluggable loader which can be registered via an entrypoint.

Usage
=====

Applications should use ``plaster`` to load settings from named sections in
a configuration source (usually a file).

Most applications will want to use
``plaster.get_settings(uri, section=None, defaults=None)`` to load the settings
from a named section. It is possible to specify the section name in the uri
itself via the ``uri#section`` syntax but it will be overridden by any explicit
``section`` parameter.

.. code-block:: python

    import plaster

    settings = plaster.get_settings('development.ini#main')

Acknowledgments
===============

This API is heavily inspired by conversations, contributions, and design put
forth in https://github.com/inklesspen/montague and
https://metaclassical.com/announcing-montague-the-new-way-to-configure-python-applications/.
