import json
from typing import Any

import requests


# TODO implement site specific post class or similar to provide an object - use markdown tokens to fetch metadata
class RestPost:
    def __init__(
        self,
        api_key: str,
        api_endpoint: str,
        title: str,
        payload: str,
        status: bool,
        tags: list[str],
        canonical_url: str,
    ) -> None:
        self.token: str = api_key
        self._api_endpoint: str = api_endpoint
        self.title: str = title
        self.payload: str = payload
        self.publish_status: bool = status
        self.canonical_url: str = canonical_url
        self.tags: str = tags
        self.headers: dict[str, str] = {
            "Content-Type": "application/json",
            "api-key": api_key,
        }

        self.build_article()

    def build_article(self) -> dict[str, Any]:
        self.payload = {
            "article": {
                "title": self.title,
                "body_markdown": f"""{self.payload}""",
                "published": self.publish_status,
                "canonical_url": self.canonical_url,
                "tags": self.tags,
            }
        }

    def upload(self) -> None:
        response: requests.Response = requests.post(
            self._api_endpoint, headers=self.headers, data=json.dumps(self.payload)
        )

        if response.status_code == 201:
            print("Article published successfully!")
            print(response.json())
        else:
            print(
                "Error publishing article. Status Code: {}".format(response.status_code)
            )
            print(response.json())
