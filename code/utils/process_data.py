import os
from typing import List
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
from unicodedata import category
import sys
from utils.constants import (
    ORIGINAL_DICT_KEY,
    PREPROCESSED_DICT_KEY,
    IMAGE_DESCRIPTION_KEY,
    IMAGE_FILE_PATH_KEY,
)
from utils.img_to_text import get_image_text_description, get_img_processor_and_model


def get_images_with_prefix(directory_path, prefix):
    """
    Returns a list of filenames in the given directory that start with the specified prefix.
    :param directory: Path to the directory
    :param prefix: The prefix to filter files
    :return: List of filenames with the specified prefix
    """
    return [
        file
        for file in os.listdir(directory_path)
        if file.startswith(prefix)
        and any(
            file.endswith(picture_extension)
            for picture_extension in ["png", "jpeg", "jpg"]
        )
    ]


def remove_files_with_extension(
    directory_path: str, file_extensions: List[str] = ["xz"]
):
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


def remove_stop_words_and_punctuations(text: str):
    codepoints = range(sys.maxunicode + 1)
    punctuations = {c for i in codepoints if category(c := chr(i)).startswith("P")}
    stop_words_and_punctuations = set(list(punctuations))
    remove_stop_words_and_tokenize = [
        i for i in word_tokenize(text) if i not in stop_words_and_punctuations
    ]

    return " ".join(
        [word for word in remove_stop_words_and_tokenize if word not in punctuations]
    )


def get_text_from_image_name_list(
    directory_path, image_file_name_list, img_processor, img_model
):
    text_description_list = []
    file_path_list = []
    for file_name in image_file_name_list:
        file_path = os.path.join(directory_path, file_name)
        description = get_image_text_description(img_processor, img_model, file_path)
        text_description_list.append(description)
        file_path_list.append(file_path)
    return text_description_list, file_path_list


def collate_post_into_preprocessed_text_array(directory_path: str):
    text_post_data_set = {ORIGINAL_DICT_KEY: [], PREPROCESSED_DICT_KEY: []}
    img_text_data_set = {IMAGE_FILE_PATH_KEY: [], IMAGE_DESCRIPTION_KEY: []}
    img_processor, img_model = get_img_processor_and_model()
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if filename.endswith("txt"):
            f = open(file_path, "r")
            # get preprocess text
            post_text = f.read()
            text_post_data_set[PREPROCESSED_DICT_KEY].append(
                remove_stop_words_and_punctuations(post_text.lower())
            )
            text_post_data_set[ORIGINAL_DICT_KEY].append(post_text)

            # preprocess images and convert them to text
            img_file_names = get_images_with_prefix(directory_path, filename[:-4])
            text_description_list, file_path_list = get_text_from_image_name_list(
                directory_path, img_file_names, img_processor, img_model
            )
            img_text_data_set[IMAGE_DESCRIPTION_KEY].append(text_description_list)
            img_text_data_set[IMAGE_FILE_PATH_KEY].append(file_path_list)

    return text_post_data_set, img_text_data_set


def process_files(directory_path):
    remove_files_with_extension(directory_path)
    text_post_data_set, img_text_data_set = collate_post_into_preprocessed_text_array(
        directory_path
    )
    return text_post_data_set, img_text_data_set


# collate_post_into_preprocessed_text_array(
#     "/Users/chungewang/Documents/classes/text_info_sys/cs410-final-proj/code/mike.natter"
# )
