"""
"""

import re


class Email:
    """
    """

    SUBJECT_KEYWORD = "subject"

    SUBJECT_PATTERN = re.compile(SUBJECT_KEYWORD, re.IGNORECASE)

    def __init__(self, content):
        """
        """

        parts = content.split("\n", 1)

        subject, count = re.subn(Email.SUBJECT_PATTERN, "", parts[0], 1)

        if count == 1:

            self._subject = subject.strip(" ").lstrip(":").lstrip(" ")
            self._body = parts[1].strip(" ")

        else:

            self._subject = ""
            self._body = content.strip(" ")

    def get_subject(self):
        """
        """

        return self._subject

    def set_subject(self, subject):
        """
        """

        self._subject = subject

    def get_body(self):
        """
        """

        return self._body

    def set_body(self, body):
        """
        """

        self._body = body
