"""
"""

import argparse
import sys

from commands.info import InfoCommand

from commands.scan import ScanCommand


if __name__ == "__main__":
    """
    """

    print()

    argument_parser = argparse.ArgumentParser(
        prog="antispam-filter",
        description="Anti-Spam Filter detects Spam Emails in a provided set of emails."
    )

    argument_parser.add_argument(
        "-i", "--info",
        required=False,
        metavar="output_file",
        dest="info_output_file",
        help="write information about the application in provided output_file"
    )

    argument_parser.add_argument(
        "-s", "--scan",
        required=False,
        nargs=2,
        metavar=("directory", "output_file"),
        dest="scan_args",
        help="scan all emails (files) from provided directory and write the analysis status in provided output file"
    )

    argument_parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s " + InfoCommand.DATA["Version"]
    )

    argument_parser.add_argument(
        "-d", "--debug",
        required=False,
        action="store_true",
        help="show debug information while executing the command"
    )

    args = argument_parser.parse_args()

    if args.info_output_file is not None:

        info_command = InfoCommand(args.info_output_file, args.debug)
        info_command.execute()

        sys.exit()

    if args.scan_args is not None:

        scan_command = ScanCommand(
            args.scan_args[0], args.scan_args[1], args.debug)
        scan_command.execute(ScanCommand.RANDOM_ANALYSIS)

        sys.exit()

    argument_parser.print_help()

    print()
