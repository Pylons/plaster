.. _glossary:

Glossary
========

.. glossary::
    :sorted:

    config uri
        In most cases this is simply an absolute or relative path to a config file on the system. However, it can also be a :rfc:`1738`-style string pointing at a remote service or a specific parser without relying on the file extension. For example, ``my-ini://foo.ini`` may point to a loader named ``my-ini`` that can parse the relative ``foo.ini`` file.

    loader
        An object conforming to the :class:`plaster.ILoader` interface. A loader is responsible for locating and parsing the underlying configuration format for the given :term:`config uri`.

    loader protocol
        A :term:`loader` may implement zero or more custom named protocols. An example would be the ``wsgi`` protocol which requires that a loader implement certain methods like ``wsgi_app = get_wsgi_app(name=None, defaults=None)``.
