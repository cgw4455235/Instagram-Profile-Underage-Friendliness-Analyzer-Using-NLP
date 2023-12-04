from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from typing import Any, Tuple, Union, List
from torch import Tensor


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = (
        attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    )
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
        input_mask_expanded.sum(1), min=1e-5
    )


def load_text_similarity_models() -> Tuple[Union[Any, Any]]:
    """_summary_
    load MINI LM sentence transformer model to map sentences to a dense vector for text similarity measurement
    Returns:
        tokenizer, model
    """
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    return tokenizer, model


def get_sentence_embedding(sentences: List[str], tokenizer: Any, model: Any) -> Tensor:
    """_summary_

    Args:
        sentences: list of sentences
        tokenizer: the tokenizer to be used on the input sentences
        model: the model for transforming sentence

    Returns:
        Tensor: embedded sentence
    """
    # Tokenize sentences
    encoded_input = tokenizer(
        sentences, padding=True, truncation=True, return_tensors="pt"
    )

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)

    # Perform pooling
    sentence_embeddings = mean_pooling(model_output, encoded_input["attention_mask"])

    # Normalize embeddings
    sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
    return sentence_embeddings


def get_similarity(
    source_query: str, test_sentences: List[str], tokenizer: Any, model: Any
):
    cos = torch.nn.CosineSimilarity(dim=0)
    similarities = []
    test_sentences_embeddings = get_sentence_embedding(test_sentences, tokenizer, model)
    source_sentence_embedding = get_sentence_embedding(
        [source_query], tokenizer, model
    )[0]
    for test_sentence_embedding in test_sentences_embeddings:
        similarity = cos(source_sentence_embedding, test_sentence_embedding)
        similarities.append(similarity)
    return similarities
