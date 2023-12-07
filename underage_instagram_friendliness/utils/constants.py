from enum import Enum

ORIGINAL_DICT_KEY = "original"
PREPROCESSED_DICT_KEY = "preprocessed"
VIOLENCE_THEME_SOURCE_SENTENCE = "I like violence"
EDUCATION_THEME_SOURCE_SENTENCE = "I like educational content"
IMAGE_DESCRIPTION_KEY = "image_description_list"
IMAGE_FILE_PATH_KEY = "image_file_path_list"


class SentimentLabels(Enum):
    neutral = "NEU"
    positive = "POS"
    negative = "NEG"
