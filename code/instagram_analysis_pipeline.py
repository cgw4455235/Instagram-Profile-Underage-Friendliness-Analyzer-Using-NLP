from utils.topic_similarity import load_text_similarity_models, get_similarity
from utils.process_data import collate_post_into_preprocessed_text_array
from utils.constants import PREPROCESSED_DICT_KEY, IMAGE_DESCRIPTION_KEY
import itertools
import os
from utils.crawler import download_random_n_posts
from utils.sentiment_analysis import (
    get_sentiment_analysis_scores,
    get_sentiment_analysis_pipeline,
)
from typing import List, Tuple, Union


def instagram_analysis_pipeline(
    profile_name: str,
    topic_query: str,
    is_process_image: bool,
    current_path: str,
    get_thematic_analysis: bool = True,
    get_sentiment_analysis: bool = True,
) -> Tuple[Union[List, List, List, List]]:
    """
    The instagram_analysis_pipeline function takes in a profile name, topic query and is_process_image flag.
    It then downloads the posts from the given instagram profile if it has not been downloaded before.
    Then it collates all of the text data into two arrays: one for text posts and one for image descriptions.
    Next, it calculates similarity scores between each post/description and the topic query using BERT embeddings.
    Finally, sentiment analysis scores are calculated.

    :param profile_name: str: Specify the name of the profile to be analysed
    :param topic_query: str: Specify the topic that you want to compare your posts against
    :param is_process_image: bool: Determine if the image should be processed
    :return: A tuple of 6 lists: text_post_topic_similarity_scores, image_topic_similarity_scores, text_post_sentiment_scores, image_sentiment_scores, text_post_data_set, img_text_data_set.
    """
    text_similarity_tokenizer, text_similarity_model = load_text_similarity_models()
    sentiment_analysis_pipeline = get_sentiment_analysis_pipeline()

    if profile_name not in os.listdir(current_path):
        download_random_n_posts(5, profile_name, current_path)

    instagram_profile_data_path = current_path + "/" + profile_name
    text_post_data_set, img_text_data_set = collate_post_into_preprocessed_text_array(
        directory_path=instagram_profile_data_path, is_process_image=is_process_image
    )
    text_post_topic_similarity_scores = (
        get_similarity(
            source_query=topic_query,
            test_sentences=text_post_data_set[PREPROCESSED_DICT_KEY],
            tokenizer=text_similarity_tokenizer,
            model=text_similarity_model,
        )
        if get_thematic_analysis
        else []
    )
    image_topic_similarity_scores = (
        (
            get_similarity(
                source_query=topic_query,
                test_sentences=list(
                    itertools.chain.from_iterable(
                        img_text_data_set[IMAGE_DESCRIPTION_KEY]
                    )
                ),
                tokenizer=text_similarity_tokenizer,
                model=text_similarity_model,
            )
            if is_process_image
            else []
        )
        if get_thematic_analysis
        else []
    )

    text_post_sentiment_scores = (
        get_sentiment_analysis_scores(
            sentiment_analysis_pipeline=sentiment_analysis_pipeline,
            sentences=text_post_data_set[PREPROCESSED_DICT_KEY],
        )
        if get_sentiment_analysis
        else []
    )

    image_sentiment_scores = (
        (
            get_sentiment_analysis_scores(
                sentiment_analysis_pipeline=sentiment_analysis_pipeline,
                sentences=itertools.chain.from_iterable(
                    img_text_data_set[IMAGE_DESCRIPTION_KEY]
                ),
            )
            if is_process_image
            else []
        )
        if get_sentiment_analysis
        else []
    )

    return (
        text_post_topic_similarity_scores,
        image_topic_similarity_scores,
        text_post_sentiment_scores,
        image_sentiment_scores,
        text_post_data_set,
        img_text_data_set,
    )
