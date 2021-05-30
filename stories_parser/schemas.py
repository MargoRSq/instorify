import io

from typing import TypedDict


class Story(TypedDict):
    type: str
    url: str
    file_obj: io.BytesIO