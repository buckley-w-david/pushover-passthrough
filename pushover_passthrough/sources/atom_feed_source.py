from typing import Literal
from dataclasses import dataclass

from pushover_passthrough.jsons import BaseModel
from pushover_passthrough.pushover import PushoverMessage


@dataclass
class AtomFeedSource(BaseModel):
    url: str
    type: Literal["atom-feed"] = "atom-feed"

    def extract(self) -> list[PushoverMessage]:
        ...
