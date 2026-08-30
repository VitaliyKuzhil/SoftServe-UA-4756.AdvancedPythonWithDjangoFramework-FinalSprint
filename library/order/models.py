from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from authentication.models import CustomUser
from book.models import Book
from authentication.constants import MIN_AMOUNT_OF_BOOK



class Order(models.Model):
    """
           This class represents an Order. \n
           Attributes:
           -----------
           param book: foreign key Book
           type book: ForeignKey
           param user: foreign key CustomUser
           type user: ForeignKey
           param created_at: Describes the date when the order was created. Can't be changed.
           type created_at: int (timestamp)
           param end_at: Describes the actual return date of the book. (`None` if not returned)
           type end_at: int (timestamp)
           param plated_end_at: Describes the planned return period of the book (2 weeks from the moment of creation).
           type plated_end_at: int (timestamp)
       """
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.PROTECT, default=None, related_name='book_orders')
    copies = models.PositiveIntegerField(default=MIN_AMOUNT_OF_BOOK)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, default=None, related_name='user_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(default=None, null=True, blank=True)
    plated_end_at = models.DateTimeField(default=None)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        """
        Magic method is redefined to show all information about Book.
        :return: book id, book name, book description, book count, book authors
        """
        data = {
            "id":self.id,
            "user":self.user,
            "book":self.book,
            "created_at": str(self.created_at) if self.created_at else None,
            "end_at":str(self.end_at) if self.end_at else None,
            "plated_end_at":str(self.plated_end_at) if self.plated_end_at else None
        }

        return ", ".join(f"'{key}': {repr(value)}" if key in ("user", "book") else \
                        f"'{key}': '{value}'" if isinstance(value,str) else \
                        f"'{key}': {value}" for key, value in data.items())


    def __repr__(self):
        """
        This magic method is redefined to show class and id of Book object.
        :return: class, id
        """
        return f'{self.__class__.__name__}(id={self.id})'


    def change_order_status(self):

        if self.is_active:
            self.is_active = False
            self.end_at = timezone.now()

            self.book.count += 1

        else:
            self.is_active = True
            self.end_at = None

            self.book.count -= 1

        self.save(update_fields=['is_active', 'end_at'])
        self.book.save(update_fields=['count'])

        return self.is_active 


    def to_dict(self):
        """
                :return: order id, book id, user id, order created_at, order end_at, order plated_end_at
                :Example:
                | {
                |   'id': 8,
                |   'book': 8,
                |   'user': 8',
                |   'created_at': 1509393504,
                |   'end_at': 1509393504,
                |   'plated_end_at': 1509402866,
                | }
                """
        return {
            'id': self.id,
            'book': self.book,
            'user': self.user,
            'created_at': str(self.created_at),
            'end_at': str(self.end_at) if self.end_at else None,
            'plated_end_at': str(self.plated_end_at)
        }


    @staticmethod
    def create(user, book, plated_end_at):
        try:

            if not book.has_available_copies():
                raise ValidationError

            new_order = Order(user=user, book=book, plated_end_at=plated_end_at)
            new_order.save()

            book.count -= 1
            book.save()

        except ValidationError:
            return None

        except Exception:
            return None

        else:
            return new_order


    @staticmethod
    def get_by_id(order_id):
        return Order.objects.filter(pk=order_id).first()


    def update(self, plated_end_at=None, end_at=None, is_active=None):
        try:

            if plated_end_at:
                self.plated_end_at = plated_end_at

            if end_at:
                self.end_at = end_at

            if is_active is not None:
                self.change_order_status()

            self.save()

        except ValidationError:
            return None

        else:
            return self


    @staticmethod
    def get_all():
        return Order.objects.all()


    @staticmethod
    def get_not_returned_books():
        return Order.objects.filter(end_at=None).values()


    @staticmethod
    def delete_by_id(order_id):
        order = Order.get_by_id(order_id)

        if not order:
            return False

        order.delete()
        return True
