from utils.crawler import download_random_n_posts
from typing import List
from utils.constants import SentimentLabels
import utils.topic_types as topic_types
import os
from instagram_analysis_pipeline import instagram_analysis_pipeline
import pickle
from profile_data.baseline_profiles import (
    NEUTRAL_SENTIMENT_PROFILES,
    NEUTRAL_THEME_PROFILES,
)
import torch
from itertools import chain

SENTIMENT_BASELINE_DATASET_SUBDIR = "profile_data" + "/" + "sentiment_baseline_profiles"
RAW_SENTIMENT_BASELINE_SCORE_PICKLE_FILE_NAME = (
    "raw_baseline_sentiment_analysis_scores.pkl"
)
BASELINE_SENTIMENT_SCORE_PICKLE_FILE_NAME = "mean_baseline_neutral_sentiment_scores.pkl"

THEME_BASELINE_DATASET_SUBDIR = "profile_data" + "/" + "neutral_theme_baseline_profiles"
RAW_THEME_BASELINE_SCORE_PICKLE_FILE_NAME = "raw_baseline_neutral_theme_scores.pkl"
BASELINE_THEME_SCORE_PICKLE_FILE_NAME = "mean_baseline_neutral_theme_scores.pkl"

MEAN_TEXT_VIOLENT_SCORE_KEY = "mean_text_violent_score"
MEAN_IMG_VIOLENT_SCORE_KEY = "mean_img_violent_score"
MEAN_TEXT_EDUCATIONAL_SCORE_KEY = "mean_text_educational_score"
MEAN_IMG_EDUCATIONAL_SCORE_KEY = "mean_img_educational_score"

MEAN_POSITIVE_TEXT_SENTIMENT_SCORE_KEY = "mean_text_positive_sentiment_score"
MEAN_NEGATIVE_TEXT_SENTIMENT_SCORE_KEY = "mean_text_negative_sentiment_score"
MEAN_NEUTRAL_TEXT_SENTIMENT_SCORE_KEY = "mean_text_neutral_sentiment_score"

MEAN_POSITIVE_IMG_SENTIMENT_SCORE_KEY = "mean_img_positive_sentiment_score"
MEAN_NEGATIVE_IMG_SENTIMENT_SCORE_KEY = "mean_img_negative_sentiment_score"
MEAN_NEUTRAL_IMG_SENTIMENT_SCORE_KEY = "mean_img_neutral_sentiment_score"


def flatten_list_and_get_mean(list_of_list):
    return torch.mean(torch.FloatTensor(list(chain.from_iterable(list_of_list))))


def flatten_list(list_of_lists):
    return list(chain.from_iterable(list_of_lists))


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
        current_path + "/" + RAW_SENTIMENT_BASELINE_SCORE_PICKLE_FILE_NAME
    )
    download_folder_path = current_path + SENTIMENT_BASELINE_DATASET_SUBDIR
    if RAW_SENTIMENT_BASELINE_SCORE_PICKLE_FILE_NAME not in os.listdir(current_path):
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


def get_thematic_scores_for_list_of_profiles(profiles_to_process: List[str]):
    download_list_of_profiles(
        NEUTRAL_THEME_PROFILES,
        THEME_BASELINE_DATASET_SUBDIR,
    )

    all_educational_text_similarity_scores = []
    all_educational_img_similarity_scores = []

    all_violent_text_similarity_scores = []
    all_violent_img_similarity_scores = []
    current_path = os.path.dirname(os.path.realpath(__file__))

    # Process sentiment analysis scores
    pickle_dump_location = (
        current_path + "/" + RAW_THEME_BASELINE_SCORE_PICKLE_FILE_NAME
    )
    download_folder_path = current_path + "/" + THEME_BASELINE_DATASET_SUBDIR

    (
        _,
        violence_topic_query,
    ) = topic_types.VIOLENCE_TOPIC_NAME_AND_QUERY
    (
        _,
        education_topic_query,
    ) = topic_types.EDUCATION_TOPIC_NAME_AND_QUERY
    if RAW_THEME_BASELINE_SCORE_PICKLE_FILE_NAME not in os.listdir(current_path):
        for profile_name in profiles_to_process:
            # EDUCATION
            (
                educational_text_post_topic_similarity_scores,
                educational_image_topic_similarity_scores,
                _,
                _,
                _,
                _,
            ) = instagram_analysis_pipeline(
                profile_name=profile_name,
                topic_query=education_topic_query,
                is_process_image=True,
                current_path=download_folder_path,
                get_sentiment_analysis=False,
            )
            all_educational_text_similarity_scores.append(
                educational_text_post_topic_similarity_scores
            )
            all_educational_img_similarity_scores.append(
                educational_image_topic_similarity_scores
            )

            # VIOLENCE
            (
                violent_text_post_topic_similarity_scores,
                violent_image_topic_similarity_scores,
                _,
                _,
                _,
                _,
            ) = instagram_analysis_pipeline(
                profile_name=profile_name,
                topic_query=violence_topic_query,
                is_process_image=True,
                current_path=download_folder_path,
                get_sentiment_analysis=False,
            )
            all_violent_text_similarity_scores.append(
                violent_text_post_topic_similarity_scores
            )
            all_violent_img_similarity_scores.append(
                violent_image_topic_similarity_scores
            )
        with open(pickle_dump_location, "wb") as f:
            pickle.dump(
                [
                    all_educational_text_similarity_scores,
                    all_educational_img_similarity_scores,
                    all_violent_text_similarity_scores,
                    all_violent_img_similarity_scores,
                ],
                f,
            )


def extract_theme_score_mean_and_save_to_pickle(
    pickle_file_name: str = RAW_THEME_BASELINE_SCORE_PICKLE_FILE_NAME,
):
    current_path = os.path.dirname(os.path.realpath(__file__))
    all_theme_score_pickle_location = current_path + "/" + pickle_file_name
    means = {
        MEAN_TEXT_VIOLENT_SCORE_KEY: 0,
        MEAN_IMG_VIOLENT_SCORE_KEY: 0,
        MEAN_TEXT_EDUCATIONAL_SCORE_KEY: 0,
        MEAN_IMG_EDUCATIONAL_SCORE_KEY: 0,
    }
    with open(all_theme_score_pickle_location, "rb") as f:
        (
            all_educational_text_similarity_scores,
            all_educational_img_similarity_scores,
            all_violent_text_similarity_scores,
            all_violent_img_similarity_scores,
        ) = pickle.load(f)

    (
        means[MEAN_TEXT_VIOLENT_SCORE_KEY],
        means[MEAN_IMG_VIOLENT_SCORE_KEY],
        means[MEAN_TEXT_EDUCATIONAL_SCORE_KEY],
        means[MEAN_IMG_EDUCATIONAL_SCORE_KEY],
    ) = (
        flatten_list_and_get_mean(all_violent_text_similarity_scores),
        flatten_list_and_get_mean(all_violent_img_similarity_scores),
        flatten_list_and_get_mean(all_educational_text_similarity_scores),
        flatten_list_and_get_mean(all_educational_img_similarity_scores),
    )
    mean_pickle_location = current_path + "/" + BASELINE_THEME_SCORE_PICKLE_FILE_NAME
    with open(mean_pickle_location, "wb") as f:
        pickle.dump(
            means,
            f,
        )
    return means


def extract_sentiment_score_mean_and_save_to_pickle(
    pickle_file_name: str = RAW_SENTIMENT_BASELINE_SCORE_PICKLE_FILE_NAME,
):
    current_path = os.path.dirname(os.path.realpath(__file__))
    all_sentiment_score_pickle_location = current_path + "/" + pickle_file_name
    means = {
        MEAN_POSITIVE_TEXT_SENTIMENT_SCORE_KEY: 0,
        MEAN_NEGATIVE_TEXT_SENTIMENT_SCORE_KEY: 0,
        MEAN_NEUTRAL_TEXT_SENTIMENT_SCORE_KEY: 0,
        MEAN_POSITIVE_IMG_SENTIMENT_SCORE_KEY: 0,
        MEAN_NEGATIVE_IMG_SENTIMENT_SCORE_KEY: 0,
        MEAN_NEUTRAL_IMG_SENTIMENT_SCORE_KEY: 0,
    }

    # Read sentiment analysis scores
    with open(all_sentiment_score_pickle_location, "rb") as f:
        all_text_sentiment_scores, all_img_sentiment_scores = pickle.load(f)

    pos_text_sentiment_scores = []
    neg_text_sentiment_scores = []
    neutral_text_sentiment_scores = []

    pos_img_sentiment_scores = []
    neg_img_sentiment_scores = []
    neutral_img_sentiment_scores = []
    ## Text Score processing
    for result in flatten_list(all_text_sentiment_scores):
        label, score = result["label"], result["score"]
        if label == SentimentLabels.positive.value:
            pos_text_sentiment_scores.append(score)
        elif label == SentimentLabels.negative.value:
            neg_text_sentiment_scores.append(score)
        elif label == SentimentLabels.neutral.value:
            neutral_text_sentiment_scores.append(score)
    ## IMG Score processing
    for result in flatten_list(all_img_sentiment_scores):
        label, score = result["label"], result["score"]
        if label == SentimentLabels.positive.value:
            pos_img_sentiment_scores.append(score)
        elif label == SentimentLabels.negative.value:
            neg_img_sentiment_scores.append(score)
        elif label == SentimentLabels.neutral.value:
            neutral_img_sentiment_scores.append(score)
    # Get means
    (
        means[MEAN_POSITIVE_TEXT_SENTIMENT_SCORE_KEY],
        means[MEAN_NEGATIVE_TEXT_SENTIMENT_SCORE_KEY],
        means[MEAN_NEUTRAL_TEXT_SENTIMENT_SCORE_KEY],
        means[MEAN_POSITIVE_IMG_SENTIMENT_SCORE_KEY],
        means[MEAN_NEGATIVE_IMG_SENTIMENT_SCORE_KEY],
        means[MEAN_NEUTRAL_IMG_SENTIMENT_SCORE_KEY],
    ) = (
        torch.mean(torch.FloatTensor(pos_text_sentiment_scores)),
        torch.mean(torch.FloatTensor(neg_text_sentiment_scores)),
        torch.mean(torch.FloatTensor(neutral_text_sentiment_scores)),
        torch.mean(torch.FloatTensor(pos_img_sentiment_scores)),
        torch.mean(torch.FloatTensor(neg_img_sentiment_scores)),
        torch.mean(torch.FloatTensor(neutral_img_sentiment_scores)),
    )
    mean_pickle_location = (
        current_path + "/" + BASELINE_SENTIMENT_SCORE_PICKLE_FILE_NAME
    )
    with open(mean_pickle_location, "wb") as f:
        pickle.dump(
            means,
            f,
        )
    return means


if __name__ == "__main__":
    get_sentiment_scores_for_list_of_profiles(NEUTRAL_SENTIMENT_PROFILES)
    get_thematic_scores_for_list_of_profiles(NEUTRAL_THEME_PROFILES)
    theme_means = extract_theme_score_mean_and_save_to_pickle()
    sentiment_means = extract_sentiment_score_mean_and_save_to_pickle()
