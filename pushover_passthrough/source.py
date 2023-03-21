from typing import Union
from pushover_passthrough.sources import GoogleBooksSource
from pushover_passthrough.sources import RssFeedSource
from pushover_passthrough.sources import AtomFeedSource

Source = Union[GoogleBooksSource, RssFeedSource, AtomFeedSource]
