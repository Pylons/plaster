import abc

from .compat import add_metaclass

@add_metaclass(abc.ABCMeta)
class Loader(object):
    def __init__(self, uri):
        self.uri = uri

    @abc.abstractmethod
    def get_settings(self, section, defaults=None):
        """
        Load the settings for the named ``section``.

        The ``section`` should never be ``None``.

        Any values in ``defaults`` may be overridden prior to returning
        the final configuration dictionary.

        """

    @abc.abstractmethod
    def get_wsgi_app(self, name, defaults=None):
        """
        Load a WSGI application.

        If ``name`` is ``None`` then the loader should either use a default
        section name for the component such as ``main`` or raise a
        :class:`plaster.exceptions.NoSectionError`.

        Any values in ``defaults`` may be overridden by the loader prior to
        returning the final configuration dictionary.

        """

    @abc.abstractmethod
    def get_wsgi_server(self, name, defaults=None):
        """
        Load a server factory that accepts a WSGI application to serve forever.

        .. code-block:: python

            plaster.setup_logging(...)
            server = plaster.get_wsgi_server(...)
            app = plaster.get_wsgi_app(...)
            server(app)

        If ``name`` is ``None`` then the loader should either use a default
        section name for the component such as ``main`` or raise a
        :class:`plaster.exceptions.NoSectionError`.

        Any values in ``defaults`` may be overridden by the loader prior to
        returning the final configuration dictionary.

        """

    @abc.abstractmethod
    def get_wsgi_filter(self, name, defaults=None):
        """
        Load a WSGI filter that accepts a WSGI application and returns a new
        WSGI application.

        If ``name`` is ``None`` then the loader should either use a default
        section name for the component such as ``main`` or raise a
        :class:`plaster.exceptions.NoSectionError`.

        Any values in ``defaults`` may be overridden by the loader prior to
        returning the final configuration dictionary.

        """

    @abc.abstractmethod
    def setup_logging(self, defaults=None):
        """
        Execute the logging configuration defined in the config file.

        This function should, at least, configure the Python standard logging
        module. However, it may also be used to configure any other logging
        subsystems that serve a similar purpose.

        """
