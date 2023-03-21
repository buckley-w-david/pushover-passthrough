from datetime import datetime
from typing import Literal, Union, Optional
from dataclasses import dataclass

import httpx

from pushover_passthrough.jsons import BaseModel
from pushover_passthrough.pushover import PushoverMessage


VOLUMES = "https://www.googleapis.com/books/v1/volumes"


@dataclass
class BookReleaseSource(BaseModel):
    isbn: str
    type: Literal["google-books-release"] = "google-books-release"

    def extract(self) -> list[PushoverMessage]:
        r = httpx.get(VOLUMES, params={"q": "isbn:%s" % self.isbn})
        results = r.json()

        for item in results["items"]:
            if any(
                id["identifier"] == self.isbn
                for id in item["volumeInfo"]["industryIdentifiers"]
            ):
                published = datetime.strptime(
                    item["volumeInfo"]["publishedDate"], "%Y-%m-%d"
                )
                url = item["volumeInfo"]["canonicalVolumeLink"]
                authors = ", ".join(item["volumeInfo"]["authors"])
                msg = f"{item['volumeInfo']['title']} by {authors} is out!"

                if published < datetime.now():
                    return [
                        PushoverMessage(
                            message=msg, url=url, url_title=item["volumeInfo"]["title"]
                        )
                    ]
        return []


@dataclass
class VolumeSource(BaseModel):
    q: Optional[str] = None
    intitle: Optional[str] = None
    inauthor: Optional[str] = None
    inpublisher: Optional[str] = None
    subject: Optional[str] = None
    isbn: Optional[str] = None
    lccn: Optional[str] = None
    oclc: Optional[str] = None
    type: Literal["google-books-volume"] = "google-books-volume"

    def extract(self) -> list[PushoverMessage]:
        parts = []
        if self.q:
            parts.append(self.q)
        if self.intitle:
            parts.append("%s:%s" % ("intitle", self.intitle))
        if self.inauthor:
            parts.append("%s:%s" % ("inauthor", self.inauthor))
        if self.inpublisher:
            parts.append("%s:%s" % ("inpublisher", self.inpublisher))
        if self.subject:
            parts.append("%s:%s" % ("subject", self.subject))
        if self.isbn:
            parts.append("%s:%s" % ("isbn", self.isbn))
        if self.lccn:
            parts.append("%s:%s" % ("lccn", self.lccn))
        if self.oclc:
            parts.append("%s:%s" % ("oclc", self.oclc))
        query = "+".join(parts)
        r = httpx.get(VOLUMES, params={"q": query})
        results = r.json()
        return []


GoogleBooksSource = Union[BookReleaseSource, VolumeSource]
