from pushover_passthrough import __version__
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import httpx


@dataclass
class PushoverMessage:
    message: str
    device: Optional[str] = None
    html: Optional[bool] = None
    priority: Optional[int] = None
    sound: Optional[str] = None
    timestamp: Optional[datetime] = None
    title: Optional[str] = None
    url: Optional[str] = None
    url_title: Optional[str] = None


class PushoverApplication:
    def __init__(self, api_token):
        self.api_token = api_token

    def push(self, user: str, message: PushoverMessage | str) -> dict:
        data = {"token": self.api_token, "user": user}

        if isinstance(message, str):
            data["message"] = message
        else:
            data.update(
                message=message.message,
                device=message.device,
                html=int(message.html) if message.html else None,
                priority=message.priority,
                sound=message.sound,
                timestamp=int(message.timestamp.timestamp())
                if message.timestamp
                else None,
                title=message.title,
                url=message.url,
                url_title=message.url_title,
            )
            data = {k: v for k, v in data.items() if v is not None}

        r = httpx.post(
            "https://api.pushover.net/1/messages.json",
            json=data,
            headers={"User-Agent": "PushoverPassthrough/%s" % __version__},
        )
        return r.json()
