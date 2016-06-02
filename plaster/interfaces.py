import abc

from .compat import add_metaclass

@add_metaclass(abc.ABCMeta)
class Loader(object):
    """
    A ``Loader`` is instantiated with a path and options parsed from the
    original ``config_uri``.

    It is required to implement ``get_settings`` and ``setup_logging``.

    Optionally it may also provide other loader-specific functionality such
    as ``get_wsgi_app`` and ``get_wsgi_server`` for loading WSGI
    configurations.

    """
    def __init__(self, path, **kw):
        self.path = path
        self.options = kw

    @abc.abstractmethod
    def get_settings(self, section, defaults=None):
        """
        Load the settings for the named ``section``.

        The ``section`` should never be ``None``.

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
