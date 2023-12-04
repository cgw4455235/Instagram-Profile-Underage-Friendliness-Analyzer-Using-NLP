import utils.topic_types as topic_types
from instagram_analysis_pipeline import instagram_analysis_pipeline
import itertools
from utils.constants import ORIGINAL_DICT_KEY

if __name__ == "__main__":
    # Modify this
    profile_name = "vegasgungirl"
    topic_name, topic_query = topic_types.VIOLENCE_TOPIC_NAME_AND_QUERY

    (
        text_post_topic_similarity_scores,
        image_topic_similarity_scores,
        text_post_sentiment_scores,
        image_sentiment_scores,
        text_post_data_set,
        img_text_data_set,
    ) = instagram_analysis_pipeline(
        profile_name=profile_name, topic_query=topic_query, is_process_image=False
    )
    # print(text_post_data_set[PREPROCESSED_DICT_KEY])
    # print(img_text_data_set[IMAGE_DESCRIPTION_KEY])

    def get_max_score_and_post_data(similarity_scores, post_data):
        if post_data and isinstance(post_data[0], list):
            post_data = list(itertools.chain.from_iterable(post_data))
        max_score = max(similarity_scores)
        max_score_idx = similarity_scores.index(max_score)
        print(max_score_idx)
        return max_score, post_data[max_score_idx]

    max_score, most_likely_post = get_max_score_and_post_data(
        text_post_topic_similarity_scores, text_post_data_set[ORIGINAL_DICT_KEY]
    )
    print(most_likely_post)
