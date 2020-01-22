"""
"""

import csv
import string

from bs4 import BeautifulSoup
from io import StringIO
from nltk.corpus import stopwords


def export_to_csv(content):
    """
    """

    text_stream = StringIO()

    csv_writer = csv.writer(text_stream)

    csv_writer.writerows(content)

    text_stream.seek(0)

    return text_stream


def clean_text(content):
    """
    """

    if "<html>" in content.lower():
        content = BeautifulSoup(content, "html.parser").text

    content = "".join(
        [character if character not in string.punctuation else " " for character in content])

    content = [word for word in content.split()
               if word.lower() not in stopwords.words("english")]

    return content
