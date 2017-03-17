import abc

from .compat import add_metaclass


@add_metaclass(abc.ABCMeta)
class ILoader(object):
    """
    An abstraction over an source of configuration settings.

    It is required to implement ``get_sections``, ``get_settings`` and
    ``setup_logging``.

    Optionally it may also provide other loader-specific functionality such
    as ``get_wsgi_app`` and ``get_wsgi_server`` for loading WSGI
    configurations. Services that depend on such functionality should document
    this so that it is easy to create custom loaders.

    :ivar uri: The :class:`plaster.PlasterURL` object used to find the
        :class:`plaster.ILoaderFactory`.

    """

    @abc.abstractmethod
    def get_sections(self):
        """
        Load the list of section names available.

        """

    @abc.abstractmethod
    def get_settings(self, section=None, defaults=None):
        """
        Load the settings for the named ``section``.

        If ``section`` is not ``None`` then it will be used. Otherwise, the
        ``section`` may be populated by the fragment defined in the
        ``config_uri#fragment`` syntax. If ``section`` is still ``None`` then
        a :class:`plaster.NoSectionError` error should be raised.

        Any values in ``defaults`` may be overridden prior to returning
        the final configuration dictionary.

        """

    @abc.abstractmethod
    def setup_logging(self, defaults=None):
        """
        Execute the logging configuration defined in the config file.

        This function should, at least, configure the Python standard logging
        module. However, it may also be used to configure any other logging
        subsystems that serve a similar purpose.

        """


@add_metaclass(abc.ABCMeta)
class ILoaderFactory(object):
    @abc.abstractmethod
    def __call__(self, uri):
        """
        A factory which accepts a :class:`plaster.PlasterURL` and returns a
        :class:`plaster.ILoader` object.

        """


@add_metaclass(abc.ABCMeta)
class ILoaderInfo(object):
    """
    An info object describing a specific :class:`plaster.ILoader`.

    :ivar scheme: The full scheme of the loader.

    """

    @abc.abstractmethod
    def load(self):
        """
        Create and return an :class:`plaster.ILoader` instance.

        """
