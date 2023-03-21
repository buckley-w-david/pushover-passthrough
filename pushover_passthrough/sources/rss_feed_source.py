from typing import Literal
from dataclasses import dataclass

from pushover_passthrough.jsons import BaseModel
from pushover_passthrough.pushover import PushoverMessage


@dataclass
class RssFeedSource(BaseModel):
    url: str
    type: Literal["rss-feed"] = "rss-feed"

    def extract(self) -> list[PushoverMessage]:
        ...
