from typing import Any, Tuple, Union
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration


def get_img_processor_and_model() -> Tuple[Union[Any, Any]]:
    img_processor = BlipProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-large"
    )
    img_model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-large"
    )
    return img_processor, img_model


def get_image_text_description(img_processor: Any, img_model: Any, img_url: str) -> str:
    image = Image.open(img_url).convert("RGB")
    text = "an image about"
    input = img_processor(image, text, return_tensors="pt")

    out = img_model.generate(**input)
    description = img_processor.decode(out[0], skip_special_tokens=True)
    return description
