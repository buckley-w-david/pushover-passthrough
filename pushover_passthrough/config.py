from dataclasses import dataclass
from pathlib import Path

import tomli

from pushover_passthrough.jsons import BaseModel
from pushover_passthrough.source import Source


@dataclass
class Configuration(BaseModel):
    pushover_application_key: str
    pushover_user_token: str
    sources: list[Source]

    @staticmethod
    def load_file(file: Path | str) -> "Configuration":
        with open(file, "rb") as f:
            data = tomli.load(f)
        return Configuration.load(data)
