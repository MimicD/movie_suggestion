import logging
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from movie_ai_prompts.serializers import PromptSerializer
from .services import search_movies


logger = logging.getLogger(__name__)

class SearchMovieView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    #permission_classes = [permissions.AllowAny]

    def post(self, request):
        # Достаём текст запроса
        query_text = request.data.get("query_text")
        if not query_text:
            return Response(
                {"detail": "Query text is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Валидируем и сохраняем prompt
        serializer = PromptSerializer(data={"text": query_text})
        serializer.is_valid(raise_exception=True)
        prompt = serializer.save(author=request.user, response={})

        # Обрабатываем top_k
        top_k = request.data.get("top_k", 5)
        try:
            top_k = int(top_k)
            if not (1 <= top_k <= 10):
                return Response(
                    {"detail": "top_k must be between 1 and 10"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (ValueError, TypeError):
            return Response(
                {"detail": "Invalid top_k value"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Выполняем поиск фильмов
        try:
            search_result = search_movies(query_text, top_k)
            if isinstance(search_result, list) and search_result and "error" in search_result[0]:
                logger.error(f"Search failed for query '{query_text}': {search_result[0]['error']}")
                return Response(
                    {"detail": search_result[0]["error"]},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            prompt.response = search_result
            prompt.save()
            logger.info(f"Search completed for query '{query_text}' by user {request.user.id}")
        except Exception as e:
            logger.error(f"Search failed for query '{query_text}': {str(e)}")
            return Response(
                {"detail": "Failed to process search request"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {"detail": "Search completed successfully", "data": PromptSerializer(prompt).data},
            status=status.HTTP_201_CREATED
        )
