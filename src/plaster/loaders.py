try:
    from importlib import metadata
except ImportError:  # pragma: no cover < py38
    import importlib_metadata as metadata

from .exceptions import LoaderNotFound, MultipleLoadersFound
from .interfaces import ILoaderInfo
from .uri import parse_uri


def get_sections(config_uri):
    """
    Load the list of named sections.

    .. code-block:: python

        sections = plaster.get_sections('development.ini')
        full_config = {
            section: plaster.get_settings('development.ini', section)
            for section in sections
        }

    :param config_uri: Anything that can be parsed by
        :func:`plaster.parse_uri`.

    :returns: A list of section names in the config file.

    """
    loader = get_loader(config_uri)

    return loader.get_sections()


def get_settings(config_uri, section=None, defaults=None):
    """
    Load the settings from a named section.

    .. code-block:: python

        settings = plaster.get_settings(...)
        print(settings['foo'])

    :param config_uri: Anything that can be parsed by
        :func:`plaster.parse_uri`.

    :param section: The name of the section in the config file. If this is
        ``None`` then it is up to the loader to determine a sensible default
        usually derived from the fragment in the ``path#name`` syntax of the
        ``config_uri``.

    :param defaults: A ``dict`` of default values used to populate the
        settings and support variable interpolation. Any values in ``defaults``
        may be overridden by the loader prior to returning the final
        configuration dictionary.

    :returns: A ``dict`` of settings. This should return a dictionary object
        even if no data is available.

    """
    loader = get_loader(config_uri)

    return loader.get_settings(section, defaults)


def setup_logging(config_uri, defaults=None):
    """
    Execute the logging configuration defined in the config file.

    This function should, at least, configure the Python standard logging
    module. However, it may also be used to configure any other logging
    subsystems that serve a similar purpose.

    :param config_uri: Anything that can be parsed by
        :func:`plaster.parse_uri`.

    :param defaults: A ``dict`` of default values used to populate the
        settings and support variable interpolation. Any values in ``defaults``
        may be overridden by the loader prior to returning the final
        configuration dictionary.

    """
    loader = get_loader(config_uri)

    return loader.setup_logging(defaults)


def get_loader(config_uri, protocols=None):
    """
    Find a :class:`plaster.ILoader` object capable of handling ``config_uri``.

    :param config_uri: Anything that can be parsed by
        :func:`plaster.parse_uri`.

    :param protocols: Zero or more :term:`loader protocol` identifiers that
        the loader must implement to match the desired ``config_uri``.

    :returns: A :class:`plaster.ILoader` object.
    :raises plaster.LoaderNotFound: If no loader could be found.
    :raises plaster.MultipleLoadersFound: If multiple loaders match the
        requested criteria. If this happens, you can disambiguate the lookup
        by appending the package name to the scheme for the loader you wish
        to use. For example if ``ini`` is ambiguous then specify
        ``ini+myapp`` to use the ini loader from the ``myapp`` package.

    """
    config_uri = parse_uri(config_uri)
    requested_scheme = config_uri.scheme

    matched_loaders = find_loaders(requested_scheme, protocols=protocols)

    if len(matched_loaders) < 1:
        raise LoaderNotFound(requested_scheme, protocols=protocols)

    if len(matched_loaders) > 1:
        raise MultipleLoadersFound(
            requested_scheme, matched_loaders, protocols=protocols
        )

    loader_info = matched_loaders[0]
    loader = loader_info.load(config_uri)

    return loader


def find_loaders(scheme, protocols=None):
    """
    Find all loaders that match the requested scheme and protocols.

    :param scheme: Any valid scheme. Examples would be something like ``ini``
        or ``pastedeploy+ini``.

    :param protocols: Zero or more :term:`loader protocol` identifiers that
        the loader must implement. If ``None`` then only generic loaders will
        be returned.

    :returns: A list containing zero or more :class:`plaster.ILoaderInfo`
        objects.

    """
    # build a list of all required entry points
    matching_groups = ["plaster.loader_factory"]

    if protocols:
        matching_groups += [f"plaster.{proto}_loader_factory" for proto in protocols]
    scheme = scheme.lower()

    # if a distribution is specified then it overrides the default search
    parts = scheme.split("+", 1)

    if len(parts) == 2:
        try:
            dist = metadata.distribution(parts[0])
        except metadata.PackageNotFoundError:
            pass
        else:
            ep = _find_ep_in_dist(dist, parts[1], matching_groups)

            # if we got one or more loaders from a specific distribution
            # then they override everything else so we'll just return them
            if ep:
                return [EntryPointLoaderInfo(dist, ep, protocols)]

    return [
        EntryPointLoaderInfo(dist, ep, protocols=protocols)
        for (dist, ep) in _iter_ep_in_dists(scheme, matching_groups)
    ]


def _iter_ep_in_dists(scheme, groups):
    # XXX this is a hack to deduplicate distributions because importlib.metadata
    # does not do this for us by default, at least up to Python 3.11.
    # Specifically, if ``lib`` is symlinked to ``lib64`` then a Distribution
    # object will be returned for each path, causing duplicate entry points
    # to be found.
    #
    # See https://github.com/Pylons/plaster/issues/25
    dups = set()
    for dist in metadata.distributions():
        name = dist.metadata["Name"]
        if name in dups:  # pragma: no cover
            continue
        dups.add(name)

        ep = _find_ep_in_dist(dist, scheme, groups)
        if ep:
            yield (dist, ep)


def _find_ep_in_dist(dist, scheme, groups):
    entry_points = [
        entry_point
        for entry_point in dist.entry_points
        if entry_point.group in groups
        and (scheme is None or scheme == entry_point.name.lower())
    ]

    # verify that the entry point from each group points to the same factory
    if len({ep.value for ep in entry_points}) == 1:
        return entry_points[0]


class EntryPointLoaderInfo(ILoaderInfo):
    def __init__(self, dist, ep, protocols=None):
        self.entry_point = ep
        self.scheme = "{}+{}".format(
            dist.metadata["name"] if "name" in dist.metadata else "Unknown", ep.name
        )
        self.protocols = protocols

        self._factory = None

    @property
    def factory(self):
        if self._factory is None:
            self._factory = self.entry_point.load()

        return self._factory

    def load(self, config_uri):
        config_uri = parse_uri(config_uri)

        return self.factory(config_uri)
