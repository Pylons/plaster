=======
plaster
=======

``plaster`` is a loader interface around arbitrary config file formats. It
exists to define a common API for applications to use when they wish to load
configuration settings. The library itself does not aim to handle anything
except a basic API that applications may use to find and load configuration
settings. Any specific constraints should be implemented in a pluggable loader
which can be registered via an entrypoint.

Installation
============

Stable release
--------------

To install plaster, run this command in your terminal:

.. code-block:: console

    $ pip install plaster

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for plaster can be downloaded from the `Github repo`_.

.. code-block:: console

    $ git clone https://github.com/mmerickel/plaster.git

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ pip install -e .

.. _Github repo: https://github.com/mmerickel/plaster

Usage
=====

Loading settings
----------------

A goal of ``plaster`` is to allow a configuration source to be used for
multiple purposes. For example, an INI file is split into separate sections
which provide settings for separate applications. This works because each
application can parse the INI file easily and pull out only the section it
cares about. In order to load settings, use the :func:`plaster.get_settings`.

The application may accept a path to a config file, allowing the user to
specify the name of the section (``myapp``) to be loaded:

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

``plaster`` requires a :class:`plaster.ILoader` to provide a way to configure
Python's stdlib logging module. In order to utilize this feature, simply
call :func:`plaster.setup_logging` from your application.

.. code-block:: python

    import plaster

    config_uri = 'redis://username@password:hostname/db?opt=val'
    plaster.setup_logging(config_uri)

Finding a loader
----------------

At the heart of ``plaster`` is the ``config_uri`` format. This format is
basically ``<scheme>://<path>`` with a few variations. The ``scheme`` is used
to find a :class:`plaster.ILoader` implementation.

.. code-block:: python

    import plaster

    config_uri = 'ini+pastedeploy://development.ini#myapp'
    loader = plaster.get_loader(config_uri)
    settings = loader.get_settings()

A ``config_uri`` may be a file path or an :rfc:`3986` URI. In the case of a
file path, the file extension is used as the scheme. In either case the
scheme is the only thing that ``plaster`` cares about with respect to finding
a valid :class:`plaster.ILoader`.

If a loader is registered with a scheme containing a ``+`` character then it
will match any schemes using simply the prefix. For example, if a loader is
registered for ``ini+pastedeploy``, it will automatically match a scheme of
simply ``ini`` but ``ini+pastedeploy`` may be used to disambiguate the lookup.

Writing your own loader
-----------------------

``plaster`` finds loaders registered for the ``plaster.loader`` entry point in
your ``setup.py``:

.. code-block:: python

    from setuptools import setup

    setup(
        # ...
        entry_points={
            'plaster.loader': [
                'dict+myapp = myapp:Loader',
            ],
        },
    )

In this example the ``myapp.Loader`` class will be used as a factory for
creating :class:`plaster.ILoader` objects. Each loader is passed
a :class:`plaster.PlasterURL` instance, the result of parsing the
``config_uri`` to determine the scheme and fragment.

.. code-block:: python

    import plaster

    class Loader(plaster.ILoader):
        def __init__(self, uri):
            self.uri = uri

        def get_sections(self):
            return ['myapp', 'yourapp']

        def get_settings(self, section=None, defaults=None):
            # fallback to the fragment from config_uri if no section is given
            if section is None:
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
            else:
                raise plaster.NoSectionError(section)
            return result

This loader may then be used:

.. code-block:: python

    import plaster

    settings = plaster.get_settings('dict+myapp://', section='myapp')
    assert settings['a'] == 1

Acknowledgments
===============

This API is heavily inspired by conversations, contributions, and design put
forth in https://github.com/inklesspen/montague and
https://metaclassical.com/announcing-montague-the-new-way-to-configure-python-applications/.

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
