from utils.ai_translator import translate_to_english
from sentence_transformers import SentenceTransformer
from pgvector.django import CosineDistance
from .models import Movie

_embedder = SentenceTransformer("all-MiniLM-L6-v2")

#Translating a text prompt
def process_prompt_text(text: str):
    return translate_to_english(text)


def search_movies(query_text: str, top_k: int = 5):
    """
    Поиск фильмов по смысловому запросу.
    1. Переводим запрос на английский
    2. Делаем эмбеддинг запроса
    3. Считаем косинусное расстояние до фильмов в БД
    4. Возвращаем top_k фильмов с минимальной дистанцией
    """
    # 1. Перевод на английский
    translated = translate_to_english(query_text)

    # 2. Эмбеддинг (превращаем в list[float])
    query_embedding = _embedder.encode(translated).tolist()

    # 3. Поиск по векторному индексу
    movies = (
        Movie.objects
        .annotate(distance=CosineDistance("embedding", query_embedding))
        .order_by("distance")[:top_k]
    )

    # 4. Готовим результат
    results = []
    for movie in movies:
        results.append({
            "title": movie.title,
            "overview": movie.overview,
            "release_date": movie.release_date,
            "original_language": movie.original_language,
            "distance": movie.distance,  # чем меньше, тем ближе
        })

    return results