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
    profile_name = "vegasgungirl"

    violent_check_threshold_sensitivity = 5  # larger is less sensitive
    educational_threshold_sensitivty = 3  # larger is less sensitive

    # Do not modify this
    violent_topic_name, violent_topic_query = topic_types.VIOLENCE_TOPIC_NAME_AND_QUERY
    (
        education_topic_name,
        education_topic_query,
    ) = topic_types.EDUCATION_TOPIC_NAME_AND_QUERY
    directory = os.path.dirname(os.path.realpath(__file__))
    # Violent Theme Check
    (
        text_post_educational_topic_similarity_scores,
        image_educational_topic_similarity_scores,
        text_post_sentiment_scores,
        image_sentiment_scores,
        text_post_data_set,
        img_text_data_set,
    ) = instagram_analysis_pipeline(
        profile_name=profile_name,
        topic_query=violent_topic_query,
        is_process_image=True,
        current_path=directory + "/profile_data",
    )

    (
        most_violent_text_post,
        most_violent_img_path,
        is_violent_theme_present_in_text,
        is_violent_theme_present_in_image,
    ) = find_max_score_and_determine_if_theme_in_profile(
        violent_topic_name,
        text_post_educational_topic_similarity_scores,
        image_educational_topic_similarity_scores,
        text_post_data_set,
        img_text_data_set,
        violent_check_threshold_sensitivity,
    )

    # Educational Theme Check
    (
        text_post_educational_topic_similarity_scores,
        image_educational_topic_similarity_scores,
        _,
        _,
        text_post_data_set,
        img_text_data_set,
    ) = instagram_analysis_pipeline(
        profile_name=profile_name,
        topic_query=education_topic_query,
        is_process_image=True,
        current_path=directory + "/profile_data",
        get_sentiment_analysis=False,
    )
    (
        most_educational_text_post,
        most_educational_img_path,
        is_educational_theme_present_in_text,
        is_educational_theme_present_in_image,
    ) = find_max_score_and_determine_if_theme_in_profile(
        education_topic_name,
        text_post_educational_topic_similarity_scores,
        image_educational_topic_similarity_scores,
        text_post_data_set,
        img_text_data_set,
        educational_threshold_sensitivty,
    )

    # Negative sentiment check
    (
        most_negative_text_post,
        is_negative_sentiment_in_text_present,
    ) = find_max_negative_sentiment_score_and_determine_if_sentiment_is_present(
        sentiment_scores=text_post_sentiment_scores,
        pre_processed_posts=text_post_data_set,
        is_image=False,
    )
    (
        most_negative_img_post,
        is_negative_sentiment_in_img_present,
    ) = find_max_negative_sentiment_score_and_determine_if_sentiment_is_present(
        sentiment_scores=image_sentiment_scores,
        pre_processed_posts=img_text_data_set,
        is_image=True,
    )

    get_ui(
        violent_img_path=most_violent_img_path,
        violent_instagram_post_text=most_violent_text_post,
        profile_name=profile_name,
        educational_img_path=most_educational_img_path,
        educational_instagram_post_text=most_educational_text_post,
        negative_text_post=most_negative_text_post,
        negative_img_post=most_negative_img_post,
        is_violent_topic_in_post_text=is_violent_theme_present_in_text,
        is_violent_topic_in_post_img=is_violent_theme_present_in_image,
        is_educational_topic_in_post_text=is_educational_theme_present_in_text,
        is_educational_topic_in_post_img=is_educational_theme_present_in_image,
        is_negative_sentiment_in_text_present=is_negative_sentiment_in_text_present,
        is_negative_sentiment_in_img_present=is_negative_sentiment_in_img_present,
    )
