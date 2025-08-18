import csv
from django.core.management.base import BaseCommand
from movie_search_logic.models import Movie
from django.db import transaction
from datetime import datetime

class Command(BaseCommand):
    help = 'Import movies from a CSV file into the Movie model, skipping duplicates and invalid dates'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def is_valid_date(self, date_str):
        """Проверяет, является ли строка валидной датой в формате YYYY-MM-DD."""
        if not date_str:
            return True  # Пустая строка допустима, так как поле nullable
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def handle(self, *args, **options):
        file_path = options['file_path']
        movies = []
        skipped_duplicates = 0
        skipped_invalid_dates = 0

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                # Собираем существующие комбинации title и release_date для проверки дубликатов
                existing_movies = set(
                    Movie.objects.values_list('title', 'release_date')
                )

                for row in reader:
                    title = row.get('title')
                    release_date_str = row.get('release_date') or None

                    # Проверяем валидность даты
                    if release_date_str and not self.is_valid_date(release_date_str):
                        self.stdout.write(
                            self.style.WARNING(
                                f"Skipping row with invalid date: {title} (release_date: {release_date_str})"
                            )
                        )
                        skipped_invalid_dates += 1
                        continue

                    # Преобразуем строку даты в объект date или None
                    release_date = None
                    if release_date_str:
                        try:
                            release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
                        except ValueError:
                            # Это избыточная проверка, так как is_valid_date уже отфильтровала
                            continue

                    # Проверяем дубликаты
                    if (title, release_date) in existing_movies:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Skipping duplicate: {title} ({release_date})"
                            )
                        )
                        skipped_duplicates += 1
                        continue

                    # Добавляем фильм в список для bulk_create
                    movies.append(Movie(
                        title=title,
                        overview=row.get('overview'),
                        release_date=release_date,
                        original_language=row.get('original_language')
                    ))

                # Импортируем фильмы батчем
                if movies:
                    with transaction.atomic():
                        Movie.objects.bulk_create(movies, batch_size=1000)
                    self.stdout.write(
                        self.style.SUCCESS(f'Imported {len(movies)} movies successfully')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('No new movies to import')
                    )

                if skipped_duplicates > 0:
                    self.stdout.write(
                        self.style.WARNING(f'Skipped {skipped_duplicates} duplicate movies')
                    )
                if skipped_invalid_dates > 0:
                    self.stdout.write(
                        self.style.WARNING(f'Skipped {skipped_invalid_dates} rows with invalid dates')
                    )

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File {file_path} not found'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error during import: {str(e)}'))