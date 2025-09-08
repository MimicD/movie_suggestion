import logging
from django.core.management.base import BaseCommand
from movie_search_logic.models import Movie
from sentence_transformers import SentenceTransformer
from django.db import transaction

class Command(BaseCommand):
    help = 'Generate embeddings for movies based on title, overview, or both'

    def handle(self, *args, **options):
        # Настройка логирования
        logger = logging.getLogger(__name__)
        
        try:
            # Загружаем модель sentence-transformers
            self.stdout.write('Loading sentence-transformers model...')
            model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Получаем фильмы без эмбеддингов
            movies = Movie.objects.filter(embedding__isnull=True)
            total_movies = movies.count()
            
            if total_movies == 0:
                self.stdout.write(self.style.WARNING('No movies need embeddings'))
                return

            self.stdout.write(f'Found {total_movies} movies to process')
            
            # Собираем тексты для батчевой обработки
            texts = []
            valid_movies = []
            skipped_movies = 0
            for movie in movies:
                if movie.title and movie.overview:
                    text = f"{movie.title} {movie.overview}"
                elif movie.title:
                    text = movie.title
                elif movie.overview:
                    text = movie.overview
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Skipping movie ID {movie.id}: Both title and overview are missing"
                        )
                    )
                    skipped_movies += 1
                    continue
                
                texts.append(text)
                valid_movies.append(movie)

            if not texts:
                self.stdout.write(self.style.WARNING('No valid movies to generate embeddings'))
                return

            # Генерируем эмбеддинги батчем
            self.stdout.write('Generating embeddings...')
            embeddings = model.encode(texts, batch_size=8, show_progress_bar=True)
            
            # Сохраняем эмбеддинги
            with transaction.atomic():
                for movie, embedding in zip(valid_movies, embeddings):
                    try:
                        movie.set_embedding(embedding.tolist())
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Failed to save embedding for movie ID {movie.id}: {str(e)}"
                            )
                        )
                        logger.error(f"Error saving embedding for movie ID {movie.id}: {str(e)}")

            self.stdout.write(
                self.style.SUCCESS(f'Successfully generated embeddings for {len(valid_movies)} movies')
            )
            if skipped_movies > 0:
                self.stdout.write(
                    self.style.WARNING(f'Skipped {skipped_movies} movies with no title or overview')
                )

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error during embedding generation: {str(e)}'))
            logger.error(f'Error during embedding generation: {str(e)}')