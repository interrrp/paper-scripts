#!/usr/bin/env python3

"""Sign the EULA."""


def main() -> None:
    """Sign the EULA."""
    with open("eula.txt", "w") as file:
        file.write("eula=true")


if __name__ == "__main__":
    main()
