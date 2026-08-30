from django.db import models
from django.core.exceptions import ValidationError
from authentication.constants import MAX_BOOK_NAME, MAX_BOOK_DESCRIPTION, DEFAULT_NUMBER_OF_BOOKS
from authentication.validators import valid_book_info



class Book(models.Model):
    """
        This class represents an Author. \n
        Attributes:
        -----------
        param name: Describes name of the book
        type name: str max_length=128
        param description: Describes description of the book
        type description: str
        param count: Describes count of the book
        type count: int default=10
        param authors: list of Authors
        type authors: list->Author
    """
    name = models.CharField(blank=True, max_length=MAX_BOOK_NAME)
    description = models.CharField(blank=True, max_length=MAX_BOOK_DESCRIPTION)
    count = models.IntegerField(default=DEFAULT_NUMBER_OF_BOOKS)
    id = models.AutoField(primary_key=True)


    def __str__(self):
        """
        Magic method is redefined to show all information about Book.
        :return: book id, book name, book description, book count, book authors
        """
        data = {
            "id": self.id,
            "name":self.name,
            "description":self.description,
            "count":self.count,
            "authors":[author.id for author in self.authors.all()]
        }

        return ", ".join(f"'{key}': '{value}'" if isinstance(value, str) else f"'{key}': {value}" for key, value in data.items())


    def __repr__(self):
        """
        This magic method is redefined to show class and id of Book object.
        :return: class, id
        """
        return f"return {self.__class__.__name__} (id={self.id})"


    @staticmethod
    def get_by_id(book_id):
        """
        :param book_id: SERIAL: the id of a Book to be found in the DB
        :return: book object or None if a book with such ID does not exist
        """
        return Book.objects.filter(id=book_id).first()


    @staticmethod
    def delete_by_id(book_id):
        """
        :param book_id: an id of a book to be deleted
        :type book_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        book = Book.get_by_id(book_id)

        if not book:
            return False

        book.delete()
        return True


    @staticmethod
    def create(name, description, count=10, authors=None):
        """
        param name: Describes name of the book
        type name: str max_length=128
        param description: Describes description of the book
        type description: str
        param count: Describes count of the book
        type count: int default=10
        param authors: list of Authors
        type authors: list->Author
        :return: a new book object which is also written into the DB
        """
        try:
            valid_book_info(name, description, count)

            new_book = Book(name = name, description = description, count = count)
            new_book.save()

            if authors:
                new_book.add_authors(authors)

        except ValidationError:
            raise

        else:
            return new_book


    def to_dict(self):
        """
        :return: book id, book name, book description, book count, book authors
        :Example:
        | {
        |   'id': 8,
        |   'name': 'django book',
        |   'description': 'bla bla bla',
        |   'count': 10',
        |   'authors': []
        | }
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'count': self.count,
            'authors': [author.id for author in self.authors.all()]
            }
    

    def update(self, name=None, description=None, count=None, authors=None):
        """
        Updates book in the database with the specified parameters.\n
        param name: Describes name of the book
        type name: str max_length=128
        param description: Describes description of the book
        type description: str
        param count: Describes count of the book
        type count: int default=10
        :return: None
        """
        try:

            valid_book_info(name, description, count)

            if name:
                self.name = name

            if description:
                self.description = description

            if count:
                self.count = count

            self.save()

            if authors:
                self.authors.set(authors)

        except ValidationError:
            raise

        else:
            return self


    def has_available_copies(self):
        active_orders = self.book_orders.filter(end_at__isnull=True).count()
        return active_orders < self.count


    def add_authors(self, authors):
        """
        Add  authors to  book in the database with the specified parameters.\n
        param authors: list authors
        :return: None
        """
        if authors:
            self.authors.add(*authors)


    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all books
        """
        return Book.objects.all()
