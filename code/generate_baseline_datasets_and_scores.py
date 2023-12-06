from utils.crawler import download_random_n_posts
from typing import List
from utils.constants import SENTIMENT_LABELS
import os
from instagram_analysis_pipeline import instagram_analysis_pipeline
import pickle
from profile_data.baseline_profiles import (
    NEUTRAL_SENTIMENT_PROFILES,
    NEUTRAL_THEME_PROFILES,
)

SENTIMENT_BASELINE_DATASET_SUBDIR = "profile_data" + "/" + "sentiment_baseline_profiles"
RAW_THEME_BASELINE_SCORE_PICKLE_FILE_NAME = "raw_baseline_sentiment_analysis_scores.pkl"

THEME_BASELINE_DATASET_SUBDIR = "profile_data" + "/" + "neutral_theme_baseline_profiles"
RAW_THEME_BASELINE_SCORE_PICKLE_FILE_NAME = "raw_baseline_neutral_theme_scores.pkl"


def download_list_of_profiles(profiles: List[str], subpath: str):
    for profile_name in profiles:
        current_path = os.path.dirname(os.path.realpath(__file__)) + "/" + subpath
        if profile_name not in os.listdir(current_path):
            download_random_n_posts(5, profile_name, subpath)


def get_sentiment_scores_for_list_of_profiles(profiles_to_process: List[str]):
    download_list_of_profiles(
        NEUTRAL_SENTIMENT_PROFILES,
        SENTIMENT_BASELINE_DATASET_SUBDIR,
    )

    text_sentiment_scores = []
    img_sentiment_scores = []
    current_path = os.path.dirname(os.path.realpath(__file__))

    # Process sentiment analysis scores
    pickle_dump_location = (
        current_path + "/" + RAW_THEME_BASELINE_SCORE_PICKLE_FILE_NAME
    )
    download_folder_path = current_path + SENTIMENT_BASELINE_DATASET_SUBDIR
    if RAW_THEME_BASELINE_SCORE_PICKLE_FILE_NAME not in os.listdir(current_path):
        for profile_name in profiles_to_process:
            (
                _,
                _,
                text_post_sentiment_scores,
                image_sentiment_scores,
                _,
                _,
            ) = instagram_analysis_pipeline(
                profile_name=profile_name,
                topic_query="",
                is_process_image=True,
                current_path=download_folder_path,
                get_thematic_analysis=False,
            )
            text_sentiment_scores.append(text_post_sentiment_scores)
            img_sentiment_scores.append(image_sentiment_scores)
        with open(pickle_dump_location, "wb") as f:
            pickle.dump([text_sentiment_scores, img_sentiment_scores], f)

    # Read sentiment analysis scores
    with open(pickle_dump_location, "rb") as f:
        text_sentiment_scores, img_sentiment_scores = pickle.load(f)


def get_thematic_scores_for_list_of_profiles(profiles_to_process: List[str]):
    download_list_of_profiles(
        NEUTRAL_THEME_PROFILES,
        THEME_BASELINE_DATASET_SUBDIR,
    )

    text_similarity_scores = []
    img_similarity_scores = []
    current_path = os.path.dirname(os.path.realpath(__file__))

    # Process sentiment analysis scores
    pickle_dump_location = (
        current_path + "/" + RAW_THEME_BASELINE_SCORE_PICKLE_FILE_NAME
    )
    download_folder_path = current_path + "/" + THEME_BASELINE_DATASET_SUBDIR
    if RAW_THEME_BASELINE_SCORE_PICKLE_FILE_NAME not in os.listdir(current_path):
        for profile_name in profiles_to_process:
            (
                text_post_topic_similarity_scores,
                image_topic_similarity_scores,
                _,
                _,
                _,
                _,
            ) = instagram_analysis_pipeline(
                profile_name=profile_name,
                topic_query="",
                is_process_image=True,
                current_path=download_folder_path,
                get_thematic_analysis=False,
            )
            text_similarity_scores.append(text_post_topic_similarity_scores)
            img_similarity_scores.append(image_topic_similarity_scores)
        with open(pickle_dump_location, "wb") as f:
            pickle.dump([text_similarity_scores, img_similarity_scores], f)

    # Read sentiment analysis scores
    with open(pickle_dump_location, "rb") as f:
        text_similarity_scores, img_similarity_scores = pickle.load(f)


if __name__ == "__main__":
    # get_sentiment_scores_for_list_of_profiles(NEUTRAL_SENTIMENT_PROFILES)
    get_thematic_scores_for_list_of_profiles(NEUTRAL_THEME_PROFILES)
