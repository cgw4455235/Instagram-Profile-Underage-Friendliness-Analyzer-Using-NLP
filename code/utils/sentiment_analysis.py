from transformers import pipeline, Pipeline
from typing import List, Dict, Union


def get_sentiment_analysis_pipeline() -> Pipeline:
    sentiment_pipeline = pipeline(
        model="finiteautomata/bertweet-base-sentiment-analysis"
    )
    return sentiment_pipeline


def get_sentiment_analysis_scores(
    sentiment_analysis_pipeline: Pipeline, sentences: List[str]
) -> List[Dict[str, Union[str, float]]]:
    shortened_sentences = [
        sentence[0 : min(128, len(sentence))] for sentence in sentences
    ]
    return sentiment_analysis_pipeline(shortened_sentences)
