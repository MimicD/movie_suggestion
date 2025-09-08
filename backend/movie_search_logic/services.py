from utils.ai_translator import translate_to_english
from utils.langchain_setup import vectorstore, llm, RAG_PROMPT
from langchain.chains import RetrievalQA
import json

def search_movies(query_text: str, top_k: int = 5):
    translated = translate_to_english(query_text)
    print(f"Translated query: {translated}")

    # Парсинг exclude_terms через LLM
    parse_prompt = f"""
    Extract the main query and exclude terms from: "{translated}"
    Return JSON: {{"main_query": "positive part", "exclude_terms": ["list of exclusions"]}}
    Examples:
    Query: "superhero movies but not Superman"
    Result: {{"main_query": "superhero movies", "exclude_terms": ["Superman", "Man of Steel"]}}
    Query: "comedy but not with Adam Sandler"
    Result: {{"main_query": "comedy", "exclude_terms": ["Adam Sandler"]}}
    Query: "movie about super heroes, but not just superman"
    Result: {{"main_query": "superhero movies", "exclude_terms": ["Superman", "Man of Steel"]}}
    Query: "{translated}"
    Result:
    """
    parse_response = llm.invoke(parse_prompt).content
    print("Parse response:", parse_response)
    try:
        parsed = json.loads(parse_response.strip('```json\n').strip('\n```'))
        main_query = parsed.get("main_query", translated)
        exclude_terms = ", ".join(parsed.get("exclude_terms", []))
    except json.JSONDecodeError:
        print("Warning: Failed to parse LLM response, using fallback")
        main_query = translated
        exclude_terms = ""

    # Retrieval: Получаем топ кандидатов
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k * 3})
    docs = retriever.invoke(main_query)
    context = "\n".join([f"Title: {doc.metadata.get('title', '')}, Overview: {doc.page_content}" for doc in docs])
    print("Retrieved docs:", [doc.metadata.get('title', '') for doc in docs])

    # Формируем кастомный промпт с параметрами
    formatted_prompt = RAG_PROMPT.format(
        query=translated,
        top_k=top_k,
        exclude_terms=exclude_terms,
        context=context
    )

    # Вызываем LLM напрямую с отформатированным промптом
    result = llm.invoke(formatted_prompt).content
    print("Raw LLM result:", result)

    try:
        return json.loads(result.strip('```json\n').strip('\n```'))
    except json.JSONDecodeError:
        print("Error: LLM did not return valid JSON:", result)
        return [{"error": "Invalid LLM response", "raw": result}]