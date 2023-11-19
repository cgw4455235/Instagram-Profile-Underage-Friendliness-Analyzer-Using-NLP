from utils.topic_similarity import load_text_similarity_models, get_similarity
from utils.topic_types import (
    VIOLENCE_TOPIC_NAME_AND_QUERY,
    EDUCATION_TOPIC_NAME_AND_QUERY,
)
from utils.process_data import collate_post_into_preprocessed_text_array
from utils.constants import PREPROCESSED_DICT_KEY, IMAGE_DESCRIPTION_KEY
import itertools
import os
from utils.crawler import download_top_n_posts

if __name__ == "__main__":
    # Modify this
    profile_name = "mockingbirdhistorylessons"
    topic_name, topic_query = EDUCATION_TOPIC_NAME_AND_QUERY

    # Don't change
    text_similarity_tokenizer, text_similarity_model = load_text_similarity_models()
    current_path = os.path.dirname(os.path.realpath(__file__))

    if profile_name not in os.listdir(current_path):
        download_top_n_posts(5, profile_name)

    instagram_profile_data_path = current_path + "/" + profile_name
    text_post_data_set, img_text_data_set = collate_post_into_preprocessed_text_array(
        instagram_profile_data_path
    )

    post_topic_similarity_scores = get_similarity(
        source_query=topic_query,
        test_sentences=text_post_data_set[PREPROCESSED_DICT_KEY],
        tokenizer=text_similarity_tokenizer,
        model=text_similarity_model,
    )
    image_topic_similarity_scores = get_similarity(
        source_query=topic_query,
        test_sentences=list(
            itertools.chain.from_iterable(img_text_data_set[IMAGE_DESCRIPTION_KEY])
        ),
        tokenizer=text_similarity_tokenizer,
        model=text_similarity_model,
    )
    print(text_post_data_set[PREPROCESSED_DICT_KEY])
    print(img_text_data_set[IMAGE_DESCRIPTION_KEY])
    print(post_topic_similarity_scores)
    print(image_topic_similarity_scores)
