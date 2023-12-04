import utils.topic_types as topic_types
from instagram_analysis_pipeline import instagram_analysis_pipeline
from utils.process_data import get_max_score_and_post_data
from utils.constants import (
    ORIGINAL_DICT_KEY,
    IMAGE_FILE_PATH_KEY,
)
from user_interface.ui import get_ui

if __name__ == "__main__":
    # Modify this
    profile_name = "mmafighting"
    topic_name, topic_query = topic_types.VIOLENCE_TOPIC_NAME_AND_QUERY

    (
        text_post_topic_similarity_scores,
        image_topic_similarity_scores,
        text_post_sentiment_scores,
        image_sentiment_scores,
        text_post_data_set,
        img_text_data_set,
    ) = instagram_analysis_pipeline(
        profile_name=profile_name, topic_query=topic_query, is_process_image=True
    )

    max_text_score, most_likely_text_post = get_max_score_and_post_data(
        text_post_topic_similarity_scores, text_post_data_set[ORIGINAL_DICT_KEY]
    )
    max_img_score, most_likely_img_path = get_max_score_and_post_data(
        image_topic_similarity_scores, img_text_data_set[IMAGE_FILE_PATH_KEY]
    )
    get_ui(
        img_path=most_likely_img_path,
        instagram_post_text=most_likely_text_post,
        topic_name=topic_name,
        profile_name=profile_name,
        is_instagram_fulfilling_theme=True,
    )
