# utils/ai_translator.py
from transformers import MarianMTModel, MarianTokenizer

# Загружаем переводчик один раз при старте
MODEL_NAME = "Helsinki-NLP/opus-mt-mul-en"
_tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
_model = MarianMTModel.from_pretrained(MODEL_NAME, use_safetensors=True)

def translate_to_english(text: str) -> str:
    """
    Перевод текста с любого языка на английский (локально).
    """
    inputs = _tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated = _model.generate(**inputs)
    return _tokenizer.decode(translated[0], skip_special_tokens=True)
