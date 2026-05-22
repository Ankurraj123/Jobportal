import collections

# Patch for djongo compatibility with Python 3.10+
if not hasattr(collections, 'Iterable'):
    import collections.abc
    collections.Iterable = collections.abc.Iterable
