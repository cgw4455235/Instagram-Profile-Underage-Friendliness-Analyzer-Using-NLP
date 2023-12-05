from utils.crawler import download_random_n_posts
from typing import List
from utils.constants import SENTIMENT_LABELS
import os
from instagram_analysis_pipeline import instagram_analysis_pipeline
import pickle


SENTIMENT_BASELINE_DATASET_SUBDIR = (
    "/" + "profile_data" + "/" + "sentiment_baseline_profiles"
)
RAW_SENTIMENT_BASELINE_SCORE_PICKLE_FILE_NAME = (
    "raw_baseline_sentiment_analysis_scores.pkl"
)
emotionally_neutral_profiles = [
    "cbsnews",
    "nbcnews",
    "bbcnews",
    "cnn",
    "bostondynamicsofficial",
    "spacex",
    "revistadeck",
    "engineermechanics",
    "history",
    "theartofwar_suntzu",
    "worldofcarpentry",
    "natgeo",
    "loverofgeography",
    "geographynow_official",
    "microsoft",
    "google",
    "salesforce",
    "roasterdaily",
    "boeing",
    "comcast",
    "mit_engineering",
    "weatherchannel",
    "accuweather",
    "nat.urephotographylove",
    "historyphotographed",
    "mitmathematics",
    "financialtimes",
    "nytimes",
    "theeconomist",
    "sportscenter",
]


def download_list_of_profiles(profiles: List[str], subpath: str):
    for profile_name in profiles:
        current_path = os.path.dirname(os.path.realpath(__file__)) + subpath
        if profile_name not in os.listdir(current_path):
            download_random_n_posts(5, profile_name)


def get_sentiment_scores_for_list_of_profiles(profiles_to_process: List[str]):
    download_list_of_profiles(
        emotionally_neutral_profiles,
        SENTIMENT_BASELINE_DATASET_SUBDIR,
    )

    text_sentiment_scores = []
    img_sentiment_scores = []
    current_path = os.path.dirname(os.path.realpath(__file__))

    # Process sentiment analysis scores
    pickle_dump_location = (
        current_path + "/" + RAW_SENTIMENT_BASELINE_SCORE_PICKLE_FILE_NAME
    )
    if RAW_SENTIMENT_BASELINE_SCORE_PICKLE_FILE_NAME not in os.listdir(current_path):
        for profile_name in profiles_to_process:
            profile_data_directory = current_path + SENTIMENT_BASELINE_DATASET_SUBDIR
            (
                _,
                _,
                text_post_sentiment_scores,
                image_sentiment_scores,
                _,
                _,
            ) = instagram_analysis_pipeline(
                profile_name=profile_name,
                topic_query="",
                is_process_image=True,
                current_path=profile_data_directory,
                get_thematic_analysis=False,
            )
            text_sentiment_scores.append(text_post_sentiment_scores)
            img_sentiment_scores.append(image_sentiment_scores)
        with open(pickle_dump_location, "wb") as f:
            pickle.dump([text_sentiment_scores, img_sentiment_scores], f)

    # Read sentiment analysis scores
    with open(pickle_dump_location, "rb") as f:
        text_sentiment_scores, img_sentiment_scores = pickle.load(f)
        print(text_sentiment_scores)
        print(img_sentiment_scores)


if __name__ == "__main__":
    get_sentiment_scores_for_list_of_profiles(emotionally_neutral_profiles)
