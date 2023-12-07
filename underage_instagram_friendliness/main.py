import utils.topic_types as topic_types
from instagram_analysis_pipeline import instagram_analysis_pipeline
from user_interface.ui import get_ui
from utils.determine_underage_friendliness import (
    find_max_score_and_determine_if_theme_in_profile,
    find_max_negative_sentiment_score_and_determine_if_sentiment_is_present,
)
import os

if __name__ == "__main__":
    # Modify this
    profile_name = "mike.natter"
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

    (
        most_likely_text_post,
        most_likely_img_path,
        is_theme_present_in_text,
        is_theme_present_in_image,
    ) = find_max_score_and_determine_if_theme_in_profile(
        topic_name,
        text_post_topic_similarity_scores,
        image_topic_similarity_scores,
        text_post_data_set,
        img_text_data_set,
    )

    print(
        find_max_negative_sentiment_score_and_determine_if_sentiment_is_present(
            sentiment_scores=text_post_sentiment_scores,
            pre_processed_posts=text_post_data_set,
            is_image=False,
        )
    )
    get_ui(
        img_path=most_likely_img_path,
        instagram_post_text=most_likely_text_post,
        topic_name=topic_name,
        profile_name=profile_name,
        is_instagram_fulfilling_theme=is_theme_present_in_text
        or is_theme_present_in_image,
    )
