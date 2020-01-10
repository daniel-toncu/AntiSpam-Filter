"""
"""

import os.path
import random

from commands.base import BaseCommand

from helpers.files_helper import get_file_paths, get_file_content, set_file_content


class ScanCommand(BaseCommand):
    """
    """

    NAME = "scan"

    CLEAN_KEYWORD = "cln"
    INFECTED_KEYWORD = "inf"

    RANDOM_ANALYSIS = None

    def __init__(self, folder, output_file, debug=False):
        """
        """

        super(ScanCommand, self).__init__(debug)

        ScanCommand.RANDOM_ANALYSIS = self._analyze_email_random

        self._folder = folder
        self._output_file = output_file

    def _analyze_email_random(self, email):
        """
        """

        if bool(random.getrandbits(1)):
            return ScanCommand.CLEAN_KEYWORD

        return ScanCommand.INFECTED_KEYWORD

    def _analyze_email(self, email):
        """
        """

        pass

    def execute(self, analysis_algorithm):
        """
        """

        file_paths = get_file_paths(self._folder)

        self._print("Scanning %d emails ...\n" % len(file_paths))

        for file_path in file_paths:

            self._print("Processing email \"%s\" ..." % file_path)

            email = get_file_content(file_path)

            status = analysis_algorithm(email)
            file_name = os.path.basename(file_path)

            status_line = "%s|%s\n" % (file_name, status)

            self._print("Status Line: \"%s\"" % status_line)

            set_file_content(self._output_file, status_line, append=True)

            self._print("Done.\n")

        self._print("Done.\n")
