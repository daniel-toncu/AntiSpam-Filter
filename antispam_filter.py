# -*- coding: utf-8 -*-
"""AntiSpam-Filter.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FVwjAnIohZQT3-Dx4HdJrDBgfo0Yzx0o
"""

import csv
import nltk
import numpy as np
import os
import pandas as pd
import pickle
import random as rnd
import string
import zipfile

from bs4 import BeautifulSoup
from google.colab import files
from io import StringIO
from nltk.corpus import stopwords
from os import listdir
from os.path import isfile, isdir, join

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

FILE_ENCODING = "utf-8"

def set_file_content(file_path, content, append=False):
    """
    """

    mode = "a" if append else "w"

    with open(file_path, mode, encoding=FILE_ENCODING) as f:
        f.write(content)

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
    content = BeautifulSoup(content).text

  content = "".join([character if character not in string.punctuation else " " for character in content])

  content = [word for word in content.split() if word.lower() not in stopwords.words("english")]

  return content

uploaded_files = files.upload()

zf = zipfile.ZipFile("Lot-01.zip")
zf.extractall()

clean_emails_file_paths = get_file_paths("Lot-01/Clean")
spam_emails_file_paths = get_file_paths("Lot-01/Spam")

emails = []

emails += [[get_file_content(file_path), 0] for file_path in clean_emails_file_paths]
emails += [[get_file_content(file_path), 1] for file_path in spam_emails_file_paths]

rnd.shuffle(emails)

emails.insert(0, ["content", "spam"])

emails_csv = export_to_csv(emails)

data_frame = pd.read_csv(emails_csv)

data_frame.head(5)

data_frame.shape

data_frame.columns

data_frame.drop_duplicates(inplace=True)
data_frame.shape

data_frame.isnull().sum()

RESOURCES_DIRECTORY_PATH = ".resources"

if not os.path.exists(RESOURCES_DIRECTORY_PATH):
  os.mkdir(RESOURCES_DIRECTORY_PATH)

nltk.download("stopwords", download_dir=RESOURCES_DIRECTORY_PATH)
nltk.data.path.append(RESOURCES_DIRECTORY_PATH)

data_frame["content"].head().apply(clean_text)

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(analyzer=clean_text)
bag_of_words = vectorizer.fit_transform(data_frame["content"])

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(bag_of_words, data_frame["spam"], test_size=0.0001, random_state=0)

bag_of_words.shape

from sklearn.naive_bayes import MultinomialNB

classifier = MultinomialNB()

classifier.fit(x_train, y_train)

print(classifier.predict(x_train))
print(y_train.values)

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

prediction = classifier.predict(x_train)

print("Classification Report\n")
print(classification_report(y_train, prediction))
print()

print("Confusion Matrix\n")
print(confusion_matrix(y_train, prediction))
print()

print("Accuracy Score\n")
print(accuracy_score(y_train, prediction))
print()

print(classifier.predict(x_test))
print(y_test.values)

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

prediction = classifier.predict(x_test)

print("Classification Report\n")
print(classification_report(y_test, prediction))
print()

print("Confusion Matrix\n")
print(confusion_matrix(y_test, prediction))
print()

print("Accuracy Score\n")
print(accuracy_score(y_test, prediction))
print()

KNOWLEDGE_DIRECTORY_PATH = ".knowledge"

if not os.path.exists(KNOWLEDGE_DIRECTORY_PATH):
  os.mkdir(KNOWLEDGE_DIRECTORY_PATH)

with open(os.path.join(KNOWLEDGE_DIRECTORY_PATH, "classifier_naive_bayes_v01"), "wb") as f:
  pickle.dump(classifier, f)

with open(os.path.join(KNOWLEDGE_DIRECTORY_PATH, "count_vectorizer_v01"), "wb") as f:
  pickle.dump(vectorizer, f)

print("===")

uploaded_files = files.upload()

zf = zipfile.ZipFile("Lot-02.zip")
zf.extractall()

test_emails_file_paths = get_file_paths("Lot-02/Test")

emails = []

emails += [[get_file_content(file_path)] for file_path in test_emails_file_paths]

emails.insert(0, ["content"])

emails_csv = export_to_csv(emails)

data_frame = pd.read_csv(emails_csv)

RESOURCES_DIRECTORY_PATH = ".resources"

if not os.path.exists(RESOURCES_DIRECTORY_PATH):
  os.mkdir(RESOURCES_DIRECTORY_PATH)

nltk.download("stopwords", download_dir=RESOURCES_DIRECTORY_PATH)
nltk.data.path.append(RESOURCES_DIRECTORY_PATH)

from sklearn.naive_bayes import MultinomialNB

with open(os.path.join(KNOWLEDGE_DIRECTORY_PATH, "classifier_naive_bayes_v01"), "rb") as f:
  classifier = pickle.load(f)

with open(os.path.join(KNOWLEDGE_DIRECTORY_PATH, "count_vectorizer_v01"), "rb") as f:
  vectorizer = pickle.load(f)

from sklearn.feature_extraction.text import CountVectorizer

bag_of_words = vectorizer.transform(data_frame["content"])

prediction = classifier.predict(bag_of_words)

CLEAN_KEYWORD = "cln"
INFECTED_KEYWORD = "inf"

LABEL_TRANSLATOR = {
    0: CLEAN_KEYWORD,
    1: INFECTED_KEYWORD
}

for i in range(len(test_emails_file_paths)):

  status = LABEL_TRANSLATOR[prediction[i]]
  file_name = os.path.basename(test_emails_file_paths[i])

  status_line = "%s|%s\n" % (file_name, status)

  set_file_content("output_file", status_line, append=True)