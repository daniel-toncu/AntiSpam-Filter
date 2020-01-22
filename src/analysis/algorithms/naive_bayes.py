"""
"""

import nltk
import numpy as np
import os
import pandas as pd
import pickle
import random as rnd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from analysis.constants import *
from analysis.helpers.text_processing import export_to_csv, clean_text
from helpers.files_helper import get_file_paths, get_file_content, set_file_content


def train(home_path, lot_directory_path):
    """
    """

    resources_directory_path = os.path.join(
        home_path, RESOURCES_DIRECTORY_NAME)

    knowledge_directory_path = os.path.join(
        home_path, KNOWLEDGE_DIRECTORY_NAME)

    clean_emails_file_paths = get_file_paths(
        os.path.join(lot_directory_path, "Clean"))

    spam_emails_file_paths = get_file_paths(
        os.path.join(lot_directory_path, "Spam"))

    emails = []

    emails += [[get_file_content(file_path), 0]
               for file_path in clean_emails_file_paths]

    emails += [[get_file_content(file_path), 1]
               for file_path in spam_emails_file_paths]

    rnd.shuffle(emails)

    emails.insert(0, ["content", "spam"])

    emails_csv = export_to_csv(emails)

    data_frame = pd.read_csv(emails_csv)

    data_frame.drop_duplicates(inplace=True)

    if not os.path.exists(resources_directory_path):
        os.mkdir(resources_directory_path)

    nltk.download("stopwords", download_dir=resources_directory_path)

    nltk.data.path.append(resources_directory_path)

    vectorizer = CountVectorizer(analyzer=clean_text)

    bag_of_words = vectorizer.fit_transform(data_frame["content"])

    x_train, x_test, y_train, y_test = train_test_split(
        bag_of_words, data_frame["spam"], test_size=0.0001, random_state=0)

    classifier = MultinomialNB()

    classifier.fit(x_train, y_train)

    print(classifier.predict(x_train))
    print(y_train.values)

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

    if not os.path.exists(knowledge_directory_path):
        os.mkdir(knowledge_directory_path)

    with open(os.path.join(knowledge_directory_path, CLASSIFIER_FILE_NAME), "wb") as f:
        pickle.dump(classifier, f)

    with open(os.path.join(knowledge_directory_path, VECTORIZER_FILE_NAME), "wb") as f:
        pickle.dump(vectorizer, f)


def test(home_path, lot_directory_path, output_file):
    """
    """

    resources_directory_path = os.path.join(
        home_path, RESOURCES_DIRECTORY_NAME)

    knowledge_directory_path = os.path.join(
        home_path, KNOWLEDGE_DIRECTORY_NAME)

    test_emails_file_paths = get_file_paths(lot_directory_path)

    emails = []

    emails += [[get_file_content(file_path)]
               for file_path in test_emails_file_paths]

    emails.insert(0, ["content"])

    emails_csv = export_to_csv(emails)

    data_frame = pd.read_csv(emails_csv)

    if not os.path.exists(resources_directory_path):
        os.mkdir(resources_directory_path)

    nltk.download("stopwords", download_dir=resources_directory_path)

    nltk.data.path.append(resources_directory_path)

    with open(os.path.join(knowledge_directory_path, CLASSIFIER_FILE_NAME), "rb") as f:
        classifier = pickle.load(f)

    with open(os.path.join(knowledge_directory_path, VECTORIZER_FILE_NAME), "rb") as f:
        vectorizer = pickle.load(f)

    bag_of_words = vectorizer.transform(data_frame["content"])

    prediction = classifier.predict(bag_of_words)

    for i in range(len(test_emails_file_paths)):

        status = LABEL_TRANSLATOR[prediction[i]]
        file_name = os.path.basename(test_emails_file_paths[i])

        status_line = "%s|%s\n" % (file_name, status)

        set_file_content(output_file, status_line, append=True)
