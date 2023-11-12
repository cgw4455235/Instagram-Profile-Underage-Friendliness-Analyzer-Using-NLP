import os
from typing import List
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
from unicodedata import category
import sys

def remove_files_with_extension(directory_path: str, file_extensions: List[str]=['xz']):
    if not os.path.exists(directory_path):
        print(f"The directory {directory_path} does not exist.")
        return

    # Remove files with the specified extension
    for filename in os.listdir(directory_path):
        for extension in file_extensions:
            if filename.endswith(extension):
                file_path = os.path.join(directory_path, filename)
                os.remove(file_path)
                print(f"Removed file: {file_path}")

def combine_all_txt_files_in_directory(directory_path: str):
    all_txt = ''
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if filename.endswith('txt'):
            f = open(file_path, "r")
            all_txt += f.read()
            
    return all_txt

def remove_stop_words_and_tokenize(all_text: str):
    codepoints = range(sys.maxunicode + 1)
    punctuations = {c for i in codepoints if category(c := chr(i)).startswith("P")}
    stop_words_and_punctuations = set(stopwords.words('english') + list(punctuations))
    remove_stop_words_and_tokenize = [i.translate(str.maketrans('', '', string.punctuation)) 
                                      for i in word_tokenize(all_text.lower())
                                      if i not in stop_words_and_punctuations]

    return [word for word in remove_stop_words_and_tokenize if word not in punctuations]

def process_files(directory_path):
    remove_files_with_extension(directory_path)
    all_text = combine_all_txt_files_in_directory(directory_path)
    print(remove_stop_words_and_tokenize(all_text))

process_files('./name')