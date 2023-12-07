from generate_baseline_datasets_and_scores import *
from utils.topic_types import (
    VIOLENCE_TOPIC_NAME_AND_QUERY,
    EDUCATION_TOPIC_NAME_AND_QUERY,
)


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
