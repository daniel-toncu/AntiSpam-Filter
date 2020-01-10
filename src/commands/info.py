"""
"""

from commands.base import BaseCommand

from helpers.files_helper import set_file_content


class InfoCommand(BaseCommand):
    """
    """

    NAME = "info"

    DATA = {
        "Project": "Anti-Spam Filter",
        "StudentName": "Daniel Țoncu",
        "Alias": "Heisenberg",
        "Version": "0.9r"
    }

    def __init__(self, output_file=None, debug=False):
        """
        """

        super(InfoCommand, self).__init__(debug)

        self._output_file = output_file

    def _get_info(self):
        """
        """

        return "%s\n%s\n%s\n%s" % (
            InfoCommand.DATA["Project"],
            InfoCommand.DATA["StudentName"],
            InfoCommand.DATA["Alias"],
            InfoCommand.DATA["Version"]
        )

    def execute(self):
        """
        """

        if self._output_file is None:
            return self._get_info()

        set_file_content(self._output_file, self._get_info())

        return ""
