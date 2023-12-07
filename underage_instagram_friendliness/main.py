import utils.topic_types as topic_types
from instagram_analysis_pipeline import instagram_analysis_pipeline
from utils.process_data import get_max_score_and_post_data
from utils.constants import (
    ORIGINAL_DICT_KEY,
    IMAGE_FILE_PATH_KEY,
)
from user_interface.ui import get_ui
from utils.determine_underage_friendliness import determine_if_theme_existent
import os

if __name__ == "__main__":
    # Modify this
    profile_name = "vegasgungirl"
    topic_name, topic_query = topic_types.VIOLENCE_TOPIC_NAME_AND_QUERY
    directory = os.path.dirname(os.path.realpath(__file__))
    (
        text_post_topic_similarity_scores,
        image_topic_similarity_scores,
        text_post_sentiment_scores,
        image_sentiment_scores,
        text_post_data_set,
        img_text_data_set,
    ) = instagram_analysis_pipeline(
        profile_name=profile_name,
        topic_query=topic_query,
        is_process_image=True,
        current_path=directory + "/profile_data",
    )

    max_text_score, most_likely_text_post = get_max_score_and_post_data(
        text_post_topic_similarity_scores, text_post_data_set[ORIGINAL_DICT_KEY]
    )
    max_img_score, most_likely_img_path = get_max_score_and_post_data(
        image_topic_similarity_scores, img_text_data_set[IMAGE_FILE_PATH_KEY]
    )
    is_theme_present_in_text = determine_if_theme_existent(
        max_post_theme_score=max_text_score,
        theme=topic_name,
        threshold_percentage=10,
        is_image=False,
    )
    is_theme_present_in_image = determine_if_theme_existent(
        max_post_theme_score=max_img_score,
        theme=topic_name,
        threshold_percentage=10,
        is_image=True,
    )

    get_ui(
        img_path=most_likely_img_path,
        instagram_post_text=most_likely_text_post,
        topic_name=topic_name,
        profile_name=profile_name,
        is_instagram_fulfilling_theme=is_theme_present_in_text
        or is_theme_present_in_image,
    )
