import os
from instagram_analysis_pipeline import instagram_analysis_pipeline
import utils.topic_types as topic_types
from utils.determine_underage_friendliness import (
    find_max_score_and_determine_if_theme_in_profile,
    find_max_negative_sentiment_score_and_determine_if_sentiment_is_present,
)
from profile_data.evaluation_profiles import (
    violent_evaluation_profiles,
    educational_evaluation_profiles,
    negative_evaluation_profiles,
)
import pickle

EVALUATION_RESULT_PKL = "evaluation_results.pkl"


def evaluate_theme_efficacy(
    profile_name, theme_topic, theme_query, threshold_percentage
) -> bool:
    directory = os.path.dirname(os.path.realpath(__file__))
    (
        text_post_topic_similarity_scores,
        image_topic_similarity_scores,
        _,
        _,
        text_post_data_set,
        img_text_data_set,
    ) = instagram_analysis_pipeline(
        profile_name=profile_name,
        topic_query=theme_query,
        is_process_image=True,
        current_path=directory + "/profile_data",
        get_sentiment_analysis=False,
    )

    (
        _,
        _,
        is_theme_present_in_text,
        is_theme_present_in_image,
    ) = find_max_score_and_determine_if_theme_in_profile(
        theme_topic,
        text_post_topic_similarity_scores,
        image_topic_similarity_scores,
        text_post_data_set,
        img_text_data_set,
        threshold_percentage,
    )
    return is_theme_present_in_text or is_theme_present_in_image


def evaluate_sentiment_efficacy(profile_name) -> bool:
    directory = os.path.dirname(os.path.realpath(__file__))
    (
        _,
        _,
        text_post_sentiment_scores,
        image_sentiment_scores,
        text_post_data_set,
        img_text_data_set,
    ) = instagram_analysis_pipeline(
        profile_name=profile_name,
        topic_query="",
        is_process_image=True,
        current_path=directory + "/profile_data",
        get_thematic_analysis=False,
    )

    (
        _,
        is_negative_sentiment_in_text_present,
    ) = find_max_negative_sentiment_score_and_determine_if_sentiment_is_present(
        sentiment_scores=text_post_sentiment_scores,
        pre_processed_posts=text_post_data_set,
        is_image=False,
    )
    (
        _,
        is_negative_sentiment_in_img_present,
    ) = find_max_negative_sentiment_score_and_determine_if_sentiment_is_present(
        sentiment_scores=image_sentiment_scores,
        pre_processed_posts=img_text_data_set,
        is_image=True,
    )
    return is_negative_sentiment_in_text_present or is_negative_sentiment_in_img_present


if __name__ == "__main__":
    violent_topic_name, violent_topic_query = topic_types.VIOLENCE_TOPIC_NAME_AND_QUERY
    (
        education_topic_name,
        education_topic_query,
    ) = topic_types.EDUCATION_TOPIC_NAME_AND_QUERY
    violent_profile_analysis_results = []
    education_profile_analysis_results = []
    negative_profile_analysis_results = []

    current_path = os.path.dirname(os.path.realpath(__file__))
    pickle_dump_location = (
        current_path + "/" + "evaluation_scores" + "/" + EVALUATION_RESULT_PKL
    )
    if EVALUATION_RESULT_PKL not in os.listdir(current_path):
        for profile_name in violent_evaluation_profiles:
            violent_profile_analysis_results.append(
                evaluate_theme_efficacy(
                    profile_name, violent_topic_name, violent_topic_query, 5
                )
            )
        for profile_name in educational_evaluation_profiles:
            education_profile_analysis_results.append(
                evaluate_theme_efficacy(
                    profile_name, education_topic_name, education_topic_query, 3
                )
            )

        for profile_name in negative_evaluation_profiles:
            negative_profile_analysis_results.append(
                evaluate_sentiment_efficacy(profile_name)
            )

    with open(pickle_dump_location, "wb") as f:
        pickle.dump(
            [
                violent_profile_analysis_results,
                education_profile_analysis_results,
                negative_profile_analysis_results,
            ],
            f,
        )

    with open(pickle_dump_location, "rb") as f:
        (
            violent_profile_analysis_results,
            education_profile_analysis_results,
            negative_profile_analysis_results,
        ) = pickle.load(f)
    print(violent_profile_analysis_results)
    print(education_profile_analysis_results)
    print(negative_profile_analysis_results)
