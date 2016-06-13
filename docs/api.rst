==================
:mod:`plaster` API
==================

.. automodule:: plaster

Application API
===============

.. autofunction:: get_settings

.. autofunction:: setup_logging

.. autofunction:: get_loader

.. autofunction:: find_loaders

.. autoclass:: LoaderInfo
    :members:

Loader API
==========

.. autofunction:: parse_uri

.. autoclass:: ILoader
    :members:

.. autoclass:: ILoaderFactory
    :members:

    .. automethod:: __call__

.. autoclass:: PlasterURL
    :members:

Exceptions
==========

.. autoexception:: InvalidURI
    :members:

.. autoexception:: LoaderNotFound
    :members:

.. autoexception:: MultipleLoadersFound
    :members:

.. autoexception:: NoSectionError
    :members:
