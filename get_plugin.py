#!/usr/bin/env python3

"""Get a plugin.

Usage: ./get_plugin.py <plugin_name>
"""

import json
from sys import argv
from urllib.parse import quote
from urllib.request import Request, urlopen

SPIGET_API_URL = "https://api.spiget.org/v2"
HEADERS = {"User-Agent": "paper-scripts"}


def get_resource_id(name: str) -> int:
    """Get the resource ID of a plugin.

    Args:
        name: The name of the plugin.
    """
    with urlopen(
        Request(
            f"{SPIGET_API_URL}/search/resources/{quote(name)}?field=name&fields=id",
            headers=HEADERS,
        )
    ) as response:
        raw_data = response.read()

    data = json.loads(raw_data)

    if not isinstance((res_id := data[0]["id"]), int):
        raise ValueError(f"Could not get resource ID for name {name}")
    return res_id


def get_download_url(resource_id: int) -> str:
    """Get the download URL of a resource.

    Args:
        resource_id: The resource ID.
    """
    with urlopen(
        Request(
            f"{SPIGET_API_URL}/resources/{resource_id}/download",
            headers=HEADERS,
        )
    ) as response:
        return response.geturl()  # type: ignore[no-any-return]


def main() -> None:
    """Get a plugin."""
    if len(argv) < 2:
        print(__doc__)
        return

    plugin_name = argv[1]

    resource_id = get_resource_id(plugin_name)
    download_url = get_download_url(resource_id)

    with urlopen(Request(download_url, headers=HEADERS)) as response:
        with open(download_url.split("/")[-1], "wb") as file:
            file.write(response.read())

    print("Done")


if __name__ == "__main__":
    main()
