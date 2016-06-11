import os.path

from .compat import urlparse
from .exceptions import InvalidURI


class PlasterURL(object):
    """
    Represents the components of a URL used to locate a
    :class:`plaster.interfaces.Loader`.

    :param scheme: The name of the loader backend.

    :param path: The loader-specific path string.
      This is the entirety of the ``config_uri`` passed to
      :func:`plaster.parse_uri` without the scheme and fragment.

    :param fragment: A loader-specific default section name.
      This parameter may be used by loaders in scenarios where they provide
      APIs that support a default name. For example, a loader that provides
      ``get_wsgi_app`` may use the fragment to determine the name of the
      section containing the WSGI app if none was explicitly defined.

    """

    def __init__(self, scheme, path=None, fragment=None):
        self.scheme = scheme
        self.path = path
        self.fragment = fragment

    def __str__(self):
        result = '{0.scheme}://{0.path}'.format(self)
        if self.fragment:
            result += '#' + self.fragment
        return result


def parse_uri(config_uri):
    """
    Return a :class:`.PlasterURI` object parsed from the ``config_uri``.

    ``config_uri`` can be a relative or absolute file path such as
    ``development.ini`` or ``/path/to/development.ini``. The file must have
    an extension that can be handled by a :class:`plaster.interfaces.Loader`
    registered with the system.

    Alternatively, ``config_uri`` may be a :rfc:`1738`-style string.

    """
    if isinstance(config_uri, PlasterURL):
        return config_uri

    # check if the uri is actually a url
    parts = urlparse.urlparse(config_uri)

    if parts.scheme:
        scheme = parts.scheme
        # reconstruct the path without the scheme and fragment
        path = urlparse.ParseResult(
            scheme='',
            netloc=parts.netloc,
            path=parts.path,
            params=parts.params,
            query=parts.query,
            fragment='',
        ).geturl()
        # strip off leading //
        path = path[2:]
        fragment = parts.fragment if parts.fragment else None

    else:
        path, fragment = config_uri, None
        if '#' in config_uri:
            path, fragment = config_uri.split('#', 1)
        scheme = os.path.splitext(path)[1]
        if scheme.startswith('.'):
            scheme = scheme[1:]

    if not scheme:
        raise InvalidURI('Could not determine the loader scheme for '
                         'the supplied "config_uri".')

    return PlasterURL(
        scheme=scheme,
        path=path,
        fragment=fragment,
    )
