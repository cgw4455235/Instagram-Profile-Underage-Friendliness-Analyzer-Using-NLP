from generate_baseline_datasets_and_scores import *
from utils.topic_types import (
    VIOLENCE_TOPIC_NAME_AND_QUERY,
    EDUCATION_TOPIC_NAME_AND_QUERY,
)
from utils.constants import (
    ORIGINAL_DICT_KEY,
    IMAGE_FILE_PATH_KEY,
)
from utils.process_data import get_max_score_and_post_data
import itertools
from typing import Optional, Tuple, Union, Any


def determine_if_theme_existent(
    max_post_theme_score: int, theme: str, threshold_percentage: float, is_image: bool
):
    mean_text_score_key = ""
    mean_img_score_key = ""
    baseline_theme_scores = read_baseline_thematic_scores()
    if theme == VIOLENCE_TOPIC_NAME_AND_QUERY[0]:
        mean_text_score_key = MEAN_TEXT_VIOLENT_SCORE_KEY
        mean_img_score_key = MEAN_IMG_VIOLENT_SCORE_KEY
    elif theme == EDUCATION_TOPIC_NAME_AND_QUERY[0]:
        mean_text_score_key = MEAN_TEXT_EDUCATIONAL_SCORE_KEY
        mean_img_score_key = MEAN_IMG_EDUCATIONAL_SCORE_KEY
    else:
        raise Exception(
            ValueError("Theme type should be either violent or educational")
        )
    return (
        max_post_theme_score
        > baseline_theme_scores[mean_img_score_key].item() * (1 + threshold_percentage)
        if is_image
        else max_post_theme_score
        > baseline_theme_scores[mean_text_score_key].item() * (1 + threshold_percentage)
    )


def find_max_score_and_determine_if_theme_in_profile(
    topic_name,
    text_post_topic_similarity_scores,
    image_topic_similarity_scores,
    text_post_data_set,
    img_text_data_set,
    threshold_percentage,
):
    max_text_score, most_likely_text_post = get_max_score_and_post_data(
        text_post_topic_similarity_scores, text_post_data_set[ORIGINAL_DICT_KEY]
    )
    max_img_score, most_likely_img_path = get_max_score_and_post_data(
        image_topic_similarity_scores, img_text_data_set[IMAGE_FILE_PATH_KEY]
    )
    is_theme_present_in_text = determine_if_theme_existent(
        max_post_theme_score=max_text_score,
        theme=topic_name,
        threshold_percentage=threshold_percentage,
        is_image=False,
    )
    is_theme_present_in_image = determine_if_theme_existent(
        max_post_theme_score=max_img_score,
        theme=topic_name,
        threshold_percentage=threshold_percentage,
        is_image=True,
    )

    return (
        most_likely_text_post,
        most_likely_img_path,
        is_theme_present_in_text,
        is_theme_present_in_image,
    )


def find_max_sentiment_score(
    sentiment_scores: List[dict], posts: List[str], sentiment_label: str
) -> Tuple[Union[Optional[float], dict]]:
    if posts and isinstance(posts[0], list):
        posts = list(itertools.chain.from_iterable(posts))
    max_score = float("-inf")
    max_post_idx = -1
    for idx, score_and_label in enumerate(sentiment_scores):
        if score_and_label["label"] == sentiment_label:
            if score_and_label["score"] > max_score:
                max_score, max_post_idx = score_and_label, idx
    if max_post_idx == -1:
        return None, posts[0]
    return sentiment_scores[idx], posts[max_post_idx]


def determine_if_post_has_sentiment(
    max_label_and_score, is_image, threshold_percentage
):
    if max_label_and_score is None:
        return False
    sentiment_label = max_label_and_score["label"]
    score = max_label_and_score["score"]
    if is_image:
        baseline_score_key = MEAN_IMAGE_SENTIMENT_KEYS[sentiment_label]
    else:
        baseline_score_key = MEAN_TEXT_SENTIMENT_KEYS[sentiment_label]
    baseline_sentiment_scores = read_baseline_sentiment_scores()
    return score > baseline_sentiment_scores[baseline_score_key].item() * (
        1 + threshold_percentage
    )


def find_max_negative_sentiment_score_and_determine_if_sentiment_is_present(
    sentiment_scores: List[dict], pre_processed_posts: List[str], is_image: bool
) -> Tuple[Union[Any, bool]]:
    post_key = ORIGINAL_DICT_KEY if not is_image else IMAGE_FILE_PATH_KEY
    max_score_and_label, max_post = find_max_sentiment_score(
        sentiment_scores=sentiment_scores,
        posts=pre_processed_posts[post_key],
        sentiment_label=SentimentLabels.negative.value,
    )

    is_sentiment_present = determine_if_post_has_sentiment(
        max_label_and_score=max_score_and_label, is_image=False, threshold_percentage=0
    )

    return (
        max_post,
        is_sentiment_present,
    )
