==================
:mod:`plaster` API
==================

.. automodule:: plaster

Application API
===============

.. autofunction:: get_settings

.. autofunction:: setup_logging

.. autofunction:: get_loader

Loader API
==========

.. autofunction:: parse_uri

.. autoclass:: Loader
    :members:

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
