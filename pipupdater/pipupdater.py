"""
Copyright (C) 2024  Murdo B. Maclachlan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import subprocess
import sys

from .logger import Logger
from .utility import str_starts_with


class Updater():
    """
    The main updater class. Wraps package update-related methods, and keeps track of data on which
    updates have succeeded and which have failed.

    :param prefixes: a list of prefixes for discarding unneeded lines
    :param logger: the logger instance
    """
    def __init__(self, logger: Logger, prefixes: list[str]) -> None:
        self.logger: Logger = logger
        self.prefixes: list[str] = prefixes

        self.failed: list[list[str]] = []
        self.success: list[list[str]] = []

    def extract_package_details(self, line: str) -> list[str]:
        """
        Extracts the details of an outdated package from a given line. The details include the
        package name, its current version, and the latest version available to update to.

        :param line: the line to extract details from
        :return: the package name, the current version and the latest version
        """
        # filter out empty characters for strings that use multiple spaces for formatting purposes
        line_parts: list[str] = list(filter(lambda x: x != '', line.split(" ")))

        package: str = line_parts[0]
        current_version: str = None
        latest_version: str = None

        # handles default 'pip list --outdated' format
        if line_parts[1] == "(Current:":
            current_version = line_parts[2]
            latest_version = line_parts[4].removesuffix(")")
        # handles 'pip list --outdated format=columns' format
        else:
            current_version = line_parts[1]
            latest_version = line_parts[2]

        return [package, current_version, latest_version]

    def update_all(self) -> None:
        """
        Updates all packages using data from sys.stdin.
        """
        self.logger.new("Parsing package list...", "INFO")

        for line in sys.stdin:

            # don't try to install debug/error output
            if str_starts_with(line, prefixes):
                # slice here removes new-line character
                self.logger.new(f"Skipping line: \"{line[:len(line)-1]}\"", "DEBUG") 
                continue

            package_details: list[str] = self.extract_package_details(line)

            # installation is attempted simply by trying to install whatever comes before the first
            # space in the line, if there are any spaces
            self.update_package(package_details)

        self.logger.print_results(self.failed, self.success)

    def update_package(self, package_details: list[str]) -> None:
        """
        Attempts to update a package with a given name, using subprocess.run() to execute a pip update
        command.

        :param package: the name of the package to update
        :param logger: the logger instance
        """
        try:
            subprocess.run(["pip", "install", "-U", package_details[0]], capture_output=True)
            self.success.append(package_details)
        except Exception as e:
            self.logger.new(f"Failed to update package: {package_details[0]} ({e})", "ERROR")
            self.failed.append(package_details)


def entry_point():
    """
    Entry point for the program. Creates the logger and prefixes array and starts the main function.
    """
    logger: Logger = Logger("pipupdater")
    prefixes: list[str] = ["DEPRECATION", "ERROR", "WARNING", "Package", "-------"]

    updater: Updater = Updater(logger, prefixes)
    updater.update_all()