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


def main() -> None:
    """Update Paper."""

    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return

    version = argv[1]
    out_path = "server.jar" if len(argv) >= 2 else argv[2]

    build = latest_build(version)
    if path.exists("paper_version.txt"):
        with open("paper_version.txt", "r+") as version_file:
            if version_file.read() == f"{version}-{build}":
                print("Paper is already the latest version")
                return

    print(f"Downloading Paper version {version} build {build}")
    download(version, build, out_path)
    print("Done.")

    with open("paper_version.txt", "w+") as version_file:
        version_file.write(f"{version}-{build}")


if __name__ == "__main__":
    main()
