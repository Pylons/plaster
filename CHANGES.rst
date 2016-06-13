unreleased
==========

- Allow ``config_uri`` syntax ``scheme:path`` alongside ``scheme://path``.
  See https://github.com/mmerickel/plaster/issues/3

- Improve errors to show the user-supplied values in the error message.
  See https://github.com/mmerickel/plaster/pull/4

- Add ``plaster.find_loaders`` which can be used by people who need a way
  to recover when ambiguous loaders are discovered via ``plaster.get_loader``.
  See https://github.com/mmerickel/plaster/pull/5

- Rename ``plaster.Loader`` to ``plaster.ILoader`` to signify its purpose
  as an interface with no actual implementation.
  See https://github.com/mmerickel/plaster/pull/5

- Introduce ``plaster.ILoaderFactory`` to document what the entry point targets
  are expected to implement.
  See https://github.com/mmerickel/plaster/pull/5

0.1.0 (2016-06-12)
==================

- Initial release.
