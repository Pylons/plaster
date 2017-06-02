=======
plaster
=======

``plaster`` is a loader interface around arbitrary config file formats. It exists to define a common API for applications to use when they wish to load configuration settings. The library itself does not aim to handle anything except a basic API that applications may use to find and load configuration settings. Any specific constraints should be implemented in a pluggable loader which can be registered via an entrypoint.

The library helps your application find an appropriate loader based on a :term:`config uri` and a desired set of :term:`loader protocol` identifiers.

Some possible ``config_uri`` formats:

* ``development.ini``
* ``development.ini#myapp``
* ``development.ini?http_port=8080#main``
* ``ini://development.conf``
* ``pastedeploy+ini:///path/to/development.ini``
* ``pastedeploy+ini://development.ini#foo``
* ``egg:MyApp?debug=false#foo``

An example application that does not care what file format the settings are sourced from, as long as they are in a section named ``my-settings``:

.. code-block:: python

    import plaster
    import sys

    if __name__ == '__main__':
        config_uri = sys.argv[1]
        settings = plaster.get_settings(config_uri, 'my-settings')

This script can support any config format so long as the application (or the user) has installed the loader they expect to use. For example, ``pip install plaster_pastedeploy``. The loader is then found by :func:`plaster.get_settings` based on the specific :term:`config uri` provided. The application does not need to configure the loaders. They are discovered via `pkg_resources entrypoints <http://setuptools.readthedocs.io/en/latest/pkg_resources.html#entry-points>`__ and registered for specific schemes.

Protocols
=========

``plaster`` supports custom loader protocols which loaders may choose to implement to provide extra functionality over the basic :class:`plaster.ILoader` interface. A :term:`loader protocol` is intentionally very loosely defined but it basically boils down to a loader object that supports extra methods with agreed-upon signatures. Right now the only officially-supported protocol is ``wsgi`` which defines a loader that should implement the :class:`plaster.protocols.IWSGIProtocol` interface.

Known Loaders
=============

* `plaster_pastedeploy <https://github.com/Pylons/plaster_pastedeploy>`__ **officially supported**

  File types:

  * ``file+ini``, ``ini``, ``pastedeploy+ini``
  * ``egg``, ``pastedeploy+egg``

  Protocols:

  * ``wsgi`` - :class:`plaster.protocols.IWSGIProtocol`

Installation
============

Stable release
--------------

To install plaster, run this command in your terminal:

.. code-block:: console

    $ pip install plaster

If you don't have `pip`_ installed, this `Python installation guide`_ can guide you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for plaster can be downloaded from the `Github repo`_.

.. code-block:: console

    $ git clone https://github.com/Pylons/plaster.git

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ pip install -e .

.. _Github repo: https://github.com/Pylons/plaster

Usage
=====

Loading settings
----------------

A goal of ``plaster`` is to allow a configuration source to be used for multiple purposes. For example, an INI file is split into separate sections which provide settings for separate applications. This works because each application can parse the INI file easily and pull out only the section it cares about. In order to load settings, use the :func:`plaster.get_settings`.

The application may accept a path to a config file, allowing the user to specify the name of the section (``myapp``) to be loaded:

.. code-block:: python

    import plaster

    config_uri = 'development.ini#myapp'
    settings = plaster.get_settings(config_uri)

Alternatively, the application may depend on a specifically named section:

.. code-block:: python

    import plaster

    config_uri = 'development.ini#myapp'
    settings = plaster.get_settings(config_uri, section='thisapp')

Configuring logging
-------------------

``plaster`` requires a :term:`loader` to provide a way to configure Python's stdlib logging module. In order to utilize this feature, simply call :func:`plaster.setup_logging` from your application.

.. code-block:: python

    import plaster

    config_uri = 'redis://username@password:hostname/db?opt=val'
    plaster.setup_logging(config_uri)

Finding a loader
----------------

At the heart of ``plaster`` is the ``config_uri`` format. This format is basically ``<scheme>://<path>`` with a few variations. The ``scheme`` is used to find an :class:`plaster.ILoaderFactory`.

.. code-block:: python

    import plaster

    config_uri = 'pastedeploy+ini://development.ini#myapp'
    loader = plaster.get_loader(config_uri, protocols=['wsgi'])
    settings = loader.get_settings()

A ``config_uri`` may be a file path or an :rfc:`3986` URI. In the case of a file path, the file extension is used as the scheme. In either case the scheme and the protocols are the only items that ``plaster`` cares about with respect to finding an :class:`plaster.ILoaderFactory`.

It's also possible to lookup the exact loader by prefixing the scheme with the name of the package containing the loader:

.. code-block:: python

    settings = plaster.get_settings('plaster_pastedeploy+ini://')

Writing your own loader
-----------------------

``plaster`` finds loaders registered for the ``plaster.loader_factory`` entry point in your ``setup.py``:

.. code-block:: python

    from setuptools import setup

    setup(
        name='myapp',
        # ...
        entry_points={
            'plaster.loader_factory': [
                'dict = myapp:Loader',
            ],
        },
    )

In this example the importable ``myapp.Loader`` class will be used as :class:`plaster.ILoaderFactory` for creating :class:`plaster.ILoader` objects. Each loader is passed a :class:`plaster.PlasterURL` instance, the result of parsing the ``config_uri`` to determine the scheme and fragment.

If the loader should be found automatically via file extension then it should broadcast support for the special ``file+<extension>`` scheme. For example, to support ``development.ini`` instead of ``myscheme://development.ini`` the loader should be registered for the ``file+ini`` scheme.

.. code-block:: python

    import plaster

    class Loader(plaster.ILoader):
        def __init__(self, uri):
            self.uri = uri

        def get_sections(self):
            return ['myapp', 'yourapp']

        def get_settings(self, section=None, defaults=None):
            # fallback to the fragment from config_uri if no section is given
            if not section:
                section = self.uri.fragment
            # if section is still none we could fallback to some
            # loader-specific default

            result = {}
            if defaults is not None:
                result.update(defaults)
            if section == 'myapp':
                result.update({'a': 1})
            elif section == 'yourapp':
                result.update({'b': 1})
            return result

This loader may then be used:

.. code-block:: python

    import plaster

    settings = plaster.get_settings('dict://', section='myapp')
    assert settings['a'] == 1

    settings2 = plaster.get_settings('myapp+dict://', section='myapp')
    assert settings == settings2

Supporting a custom protocol
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, loaders are exposed via the ``plaster.loader_factory`` entry point. In order to register a loader that supports a custom protocol it should register itself on a ``plaster.<protocol>_loader_factory`` entry point.

A scheme **MUST** point to the same loader factory for every protocol, including the default (empty) protocol. If it does not then no compatible loader will be found if the end-user requests a loader satisfying both protocols.

Acknowledgments
===============

This API is heavily inspired by conversations, contributions, and design put forth in https://github.com/inklesspen/montague and https://metaclassical.com/announcing-montague-the-new-way-to-configure-python-applications/.

More Information
================

.. toctree::
   :maxdepth: 1

   api
   glossary
   contributing
   changes

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
