import pytest

from main import BooksCollector

ALLOWED_BOOKS_NAMES = ['book1', 'book2', 'book3', 'book4', 'book5']
NOT_ALLOWED_BOOKS_NAMES = ['a' * 41, 'b' * 42, 'c' * 43, 'd' * 44, 'e' * 45]

ALLOWED_GENRE = ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии']
NOT_ALLOWED_GENRE = ['genre1', 'genre2', 'genre3', 'genre4', 'genre5']

GENRE_AGE_RATING = ['Ужасы', 'Детективы']


class TestBooksCollector:       
    @pytest.fixture(scope='function')
    def books_collector(self):
        self.books_collector = BooksCollector()

    @pytest.fixture(scope='function')
    def all_genre_books_collector(self):
        self.all_genre_books_collector = BooksCollector()
        for name, genre in zip(ALLOWED_BOOKS_NAMES, ALLOWED_GENRE):
            self.all_genre_books_collector.add_new_book(name)
            self.all_genre_books_collector.set_book_genre(name, genre)

    def test_init_none_bookscollector_object(self):
        assert isinstance(BooksCollector(), BooksCollector)

    @pytest.mark.parametrize('name', ALLOWED_BOOKS_NAMES)
    def test_add_new_book_allowed_book_name_book_in_books_genre(self, name, books_collector):
        self.books_collector.add_new_book(name)
        assert name in self.books_collector.books_genre

    @pytest.mark.parametrize('name, genre', [*zip(ALLOWED_BOOKS_NAMES, NOT_ALLOWED_GENRE)])
    def test_set_book_genre_genre_not_allowed_book_genre_has_empty_str(self, name, genre, books_collector):
        self.books_collector.add_new_book(name)
        old_genre = self.books_collector.books_genre[name]
        self.books_collector.set_book_genre(name, genre)
        assert self.books_collector.books_genre[name] == old_genre

    @pytest.mark.parametrize('name, genre', [*zip(ALLOWED_BOOKS_NAMES, ALLOWED_GENRE)])
    def test_get_book_genre_add_book_with_genre_eq_genre(self, name, genre, books_collector):
        self.books_collector.add_new_book(name)
        self.books_collector.set_book_genre(name, genre)
        assert self.books_collector.get_book_genre(name) == genre

    @pytest.mark.parametrize('bad_genre', NOT_ALLOWED_GENRE)
    def test_get_books_with_specific_genre_genre_not_allowed_empty_list(self, bad_genre, all_genre_books_collector):
        assert self.all_genre_books_collector.get_books_with_specific_genre(bad_genre) == []

    def test_get_books_genre_allowed_books_genre_eq_allowed_genre(self, all_genre_books_collector):
        allowed_books_genre = {book: genre for book, genre in zip(ALLOWED_BOOKS_NAMES, ALLOWED_GENRE)}
        assert self.all_genre_books_collector.get_books_genre() == allowed_books_genre

    def test_get_books_for_children_all_genre_books_age_rating_books(self, all_genre_books_collector):
        children_books = [
            book for book, genre in zip(ALLOWED_BOOKS_NAMES, ALLOWED_GENRE)
            if genre not in GENRE_AGE_RATING
        ]
        assert self.all_genre_books_collector.get_books_for_children() == children_books

    @pytest.mark.parametrize('name', NOT_ALLOWED_BOOKS_NAMES)
    def test_add_book_in_favorites_name_already_added_favorites_same(self, name, all_genre_books_collector):
        favorites = self.all_genre_books_collector.favorites.copy()

        self.all_genre_books_collector.add_book_in_favorites(name)
        assert self.all_genre_books_collector.favorites == favorites

    @pytest.mark.parametrize('name', ALLOWED_BOOKS_NAMES)
    def test_delete_book_from_favorites_book_name_not_in_favorites(self, name, all_genre_books_collector):
        self.all_genre_books_collector.delete_book_from_favorites(name)
        assert name not in self.all_genre_books_collector.favorites

    @pytest.mark.parametrize('name', ALLOWED_BOOKS_NAMES)
    def test_get_list_of_favorites_books_favorite_book_list_with_book(self, name, all_genre_books_collector):
        self.all_genre_books_collector.add_book_in_favorites(name)
        assert self.all_genre_books_collector.get_list_of_favorites_books() == [name]
