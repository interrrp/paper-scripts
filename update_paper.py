#!/usr/bin/env python3

"""Update Paper.

This will download the latest build of the given version to out_path, and write
the version and build number to paper_version.txt.

Usage: python update_paper.py <version> [out_path=server.jar]
"""

import json
import urllib.request
from os import path
from sys import argv

API_URL = "https://api.papermc.io/v2/projects/paper"


def latest_build(version: str) -> int:
    """Get the latest build number for the given version."""
    url = f"{API_URL}/versions/{version}"
    with urllib.request.urlopen(url) as response:
        raw_data = response.read()
        data = json.loads(raw_data)

    if (
        "builds" not in data
        or not data["builds"]
        or not isinstance(data["builds"][-1], int)
    ):
        raise KeyError(f"There are no builds for version {version}")

    return data["builds"][-1]


def download(version: str, build: int, out_path: str = "server.jar") -> None:
    """Download a Paper server JAR."""
    url = (
        f"{API_URL}/versions/{version}/builds/{build}/downloads/paper-"
        f"{version}-{build}.jar"
    )
    with urllib.request.urlopen(url) as response:
        with open(out_path, "wb") as file:
            file.write(response.read())


def write_paper_version(version: str, build: int) -> None:
    """Write to the Paper version file."""
    with open("paper_version.txt", "w+") as version_file:
        version_file.write(f"{version}-{build}")


def read_paper_version() -> tuple[str, int]:
    """Read the Paper version file.

    This returns a tuple containing the version and the build number.
    """
    with open("paper_version.txt", "r") as version_file:
        version, build = version_file.read().split("-")

    return version, int(build)


def main() -> None:
    """Update Paper."""
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return

    version = argv[1]
    out_path = "server.jar" if len(argv) >= 2 else argv[2]

    build = latest_build(version)
    if path.exists("paper_version.txt"):
        if read_paper_version() == (version, build):
            print("Paper is already on the latest version")
            return

    print(f"Downloading Paper version {version} build {build}")
    download(version, build, out_path)
    print("Done.")

    write_paper_version(version, build)


if __name__ == "__main__":
    main()
