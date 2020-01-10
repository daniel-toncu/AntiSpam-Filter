"""
"""

from os import listdir
from os.path import isfile, isdir, join


FILE_ENCODING = "utf-8"


def get_file_paths(directory_path):
    """
    """

    if not isdir(directory_path):
        raise Exception("Given path does not refer to a valid directory.")

    file_paths = [join(directory_path, f) for f in listdir(
        directory_path) if isfile(join(directory_path, f))]

    return file_paths


def get_file_content(file_path):
    """
    """

    with open(file_path, "r", encoding="ISO-8859-1") as f:
        return f.read()


def set_file_content(file_path, content, append=False):
    """
    """

    mode = "a" if append else "w"

    with open(file_path, mode, encoding=FILE_ENCODING) as f:
        f.write(content)
