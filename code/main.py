from utils.topic_similarity import load_text_similarity_models, get_similarity
import utils.topic_types as topic_types
from instagram_analysis_pipeline import instagram_analysis_pipeline

if __name__ == "__main__":
    # Modify this
    profile_name = "britishlibrary"
    topic_name, topic_query = topic_types.EDUCATION_TOPIC_NAME_AND_QUERY

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
    print(text_post_topic_similarity_scores)
    print(image_topic_similarity_scores)

    print(text_post_sentiment_scores)
    print(image_sentiment_scores)
