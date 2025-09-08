from django.urls import path
from .views import SearchMovieView

urlpatterns = [
    path('search_movie/', SearchMovieView.as_view(), name= "search-movie")
]
