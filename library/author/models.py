from django.db import models
from django.core.exceptions import ValidationError
from authentication.validators import valid_bio_info
from authentication.constants import MAX_NAME_CHARACTERS
import book.models



class Author(models.Model):
    """
        This class represents an Author. \n
        Attributes:
        -----------
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes last name of the author
        type surname: str max_length=20
        param patronymic: Describes middle name of the author
        type patronymic: str max_length=20
    """
    name = models.CharField(blank=True, max_length=MAX_NAME_CHARACTERS)
    surname = models.CharField(blank=True, max_length=MAX_NAME_CHARACTERS)
    patronymic = models.CharField(blank=True, max_length=MAX_NAME_CHARACTERS)
    books = models.ManyToManyField(book.models.Book, blank=True, related_name='authors')
    id = models.AutoField(primary_key=True)


    def __str__(self):
        """
        Magic method is redefined to show all information about Author.
        :return: author id, author name, author surname, author patronymic
        """
        data = {
            "id": self.id,
            "name":self.name,
            "surname":self.surname,
            "patronymic":self.patronymic
        }

        return ", ".join(f"'{key}': '{value}'" if isinstance(value, str) else f"'{key}': {value}" for key, value in data.items())


    def __repr__(self):
        """
        This magic method is redefined to show class and id of Author object.
        :return: class, id
        """
        return f"{self.__class__.__name__} (id={self.pk})"


    @staticmethod
    def get_by_id(author_id):
        """
        :param author_id: SERIAL: the id of a Author to be found in the DB
        :return: author object or None if a user with such ID does not exist
        """
        return Author.objects.filter(id=author_id).first()


    @staticmethod
    def delete_by_id(author_id):
        """
        :param author_id: an id of a author to be deleted
        :type author_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        author = Author.get_by_id(author_id)

        if not author:
            return False

        author.delete()
        return True


    @staticmethod
    def create(name, surname, patronymic):
        """
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes surname of the author
        type surname: str max_length=20
        param patronymic: Describes patronymic of the author
        type patronymic: str max_length=20
        :return: a new author object which is also written into the DB
        """
        try:
            valid_bio_info(name, surname, patronymic)

            new_author = Author(name=name, surname=surname, patronymic=patronymic)
            new_author.save()

        except ValidationError:
            raise

        else:
            return new_author


    def to_dict(self):
        """
        :return: author id, author name, author surname, author patronymic
        :Example:
        | {
        |   'id': 8,
        |   'name': 'fn',
        |   'surname': 'mn',
        |   'patronymic': 'ln',
        | }
        """
        return self.__dict__


    def update(self,
               name=None,
               surname=None,
               patronymic=None):
        """
        Updates author in the database with the specified parameters.\n
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes surname of the author
        type surname: str max_length=20
        param patronymic: Describes patronymic of the author
        type patronymic: str max_length=20
        :return: None
        """

        try:
            valid_bio_info(name, surname, patronymic)

            if name:
                self.name = name

            if surname:
                self.surname = surname

            if patronymic:
                self.patronymic = patronymic

            self.save()

        except ValidationError:
            raise

        else:
            return self


    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all authors
        """
        return Author.objects.all()
