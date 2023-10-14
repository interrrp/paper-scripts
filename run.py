#!/usr/bin/env python3

"""Run the server.

Usage: ./run.py [jar_path=server.jar] [ram_gb=2] [java=java]
"""

from subprocess import run
from sys import argv


def main() -> None:
    """Run the server."""
    if len(argv) > 1 and argv[1] in ("-h", "--help"):
        print(__doc__)
        return

    ram_gb = 2 if len(argv) < 2 else int(argv[1])
    jar_path = "server.jar" if len(argv) < 3 else argv[2]
    java = "java" if len(argv) < 4 else argv[3]

    run([java, f"-Xmx{ram_gb}G", f"-Xms{ram_gb}G", "-jar", jar_path, "--nogui"])


if __name__ == "__main__":
    main()
