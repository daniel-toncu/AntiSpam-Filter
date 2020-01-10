"""
"""


class BaseCommand:
    """
    """

    def __init__(self, debug=False):
        """
        """

        self._debug = debug

    def _print(self, message):
        """
        """

        if self._debug:
            print(" DEBUG: %s" % message)

    def execute(self):
        """
        """

        raise NotImplementedError()
