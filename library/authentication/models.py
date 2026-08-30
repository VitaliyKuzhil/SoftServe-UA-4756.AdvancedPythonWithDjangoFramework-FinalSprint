import datetime
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from authentication.constants import ROLE_CHOICES, MAX_EMAIL_CHARACTERS, MAX_NAME_CHARACTERS, MAX_PASSWORD_CHARACTERS, MIN_PASSWORD_CHARACTERS
from authentication.validators import valid_email, valid_bio_info



class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 1)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractBaseUser):
    """
        This class represents a basic user. \n
        Attributes:
        -----------
        param first_name: Describes first name of the user
        type first_name: str max length=20
        param last_name: Describes last name of the user
        type last_name: str max length=20
        param middle_name: Describes middle name of the user
        type middle_name: str max length=20
        param email: Describes the email of the user
        type email: str, unique, max length=100
        param password: Describes the password of the user
        type password: str
        param created_at: Describes the date when the user was created. Can't be changed.
        type created_at: int (timestamp)
        param updated_at: Describes the date when the user was modified
        type updated_at: int (timestamp)
        param role: user role, default role (0, 'visitor')
        type updated_at: int (choices)
        param is_active: user role, default value False
        type updated_at: bool
    """
    first_name = models.CharField(max_length=MAX_NAME_CHARACTERS, null=True, blank=True, default=None)
    last_name = models.CharField(max_length=MAX_NAME_CHARACTERS, null=True, blank=True,default=None)
    middle_name = models.CharField(max_length=MAX_NAME_CHARACTERS, null=True, blank=True, default=None)

    email = models.EmailField(max_length=MAX_EMAIL_CHARACTERS, unique=True, default=None)
    password = models.CharField(default=None, max_length=MAX_PASSWORD_CHARACTERS, 
                                validators=[MinLengthValidator(MIN_PASSWORD_CHARACTERS)])

    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    role = models.IntegerField(choices=ROLE_CHOICES, default=0)

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    id = models.AutoField(primary_key=True)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()


    def __str__(self):
        """
        Magic method is redefined to show all information about CustomUser.
        :return: user id, user first_name, user middle_name, user last_name,
                 user email, user password, user updated_at, user created_at,
                 user role, user is_active
        """
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': int(self.created_at.timestamp()),
            'updated_at': int(self.updated_at.timestamp()),
            'role': self.role,
            'is_active': self.is_active
        }

        return ", ".join(f"'{key}': '{value}'" if isinstance(value, str) else f"'{key}': {value}" for key, value in data.items())


    def __repr__(self):
        """
        This magic method is redefined to show class and id of CustomUser object.
        :return: class, id
        """
        return f"{self.__class__.__name__}(id={self.id}, role={self.get_role_name()})"


    @property
    def is_staff(self):
        return self.role == 1 or self.is_superuser


    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        return self.role == 1 and self.is_active


    def has_perms(self, perm, obj=None):
        if self.is_superuser:
            return True
        return self.role == 1 and self.is_active


    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        return self.role == 1 and self.is_active


    @staticmethod
    def get_by_id(user_id):
        """
        :param user_id: SERIAL: the id of a user to be found in the DB
        :return: user object or None if a user with such ID does not exist
        """
        return CustomUser.objects.filter(id=user_id).first()


    @staticmethod
    def get_by_email(email):
        """
        Returns user by email
        :param email: email by which we need to find the user
        :type email: str
        :return: user object or None if a user with such ID does not exist
        """
        return CustomUser.objects.filter(email=email).first()


    @staticmethod
    def delete_by_id(user_id):
        """
        :param user_id: an id of a user to be deleted
        :type user_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        user_to_delete = CustomUser.objects.filter(id=user_id).first()

        if user_to_delete:
            CustomUser.objects.filter(id=user_id).delete()
            return True

        return False


    @classmethod
    def create(cls, email, password, first_name=None, middle_name=None, last_name=None):
        """
        :param first_name: first name of a user
        :type first_name: str
        :param middle_name: middle name of a user
        :type middle_name: str
        :param last_name: last name of a user
        :type last_name: str
        :param email: email of a user
        :type email: str
        :param password: password of a user
        :type password: str
        :return: a new user object which is also written into the DB
        """
        try:
            if cls.objects.filter(email=email).exists():
                raise ValidationError

            valid_email(email)
            valid_bio_info(first_name, last_name, middle_name)
            validate_password(password)
            
            new_user = cls.objects.create(
                email = email,
                first_name = first_name,
                last_name = last_name,
                middle_name = middle_name
            )

            new_user.set_password(password)
            new_user.save()

        except ValidationError:
            raise

        else:
            return new_user


    def to_dict(self):
        """
        :return: user id, user first_name, user middle_name, user last_name,
                 user email, user password, user updated_at, user created_at, user is_active
        :Example:
        | {
        |   'id': 8,
        |   'first_name': 'fn',
        |   'middle_name': 'mn',
        |   'last_name': 'ln',
        |   'email': 'ln@mail.com',
        |   'created_at': 1509393504,
        |   'updated_at': 1509402866,
        |   'role': 0
        |   'is_active:' True
        | }
        """
        return {'id': self.id,
                'first_name': self.first_name,
                'middle_name': self.middle_name,
                'last_name': self.last_name,
                'email': self.email,
                'created_at': int(self.created_at.timestamp()),
                'updated_at': int(self.updated_at.timestamp()),
                'role': self.role,
                'is_active': self.is_active
                }


    def update(self,
               first_name=None,
               last_name=None,
               middle_name=None,
               password=None,
               role=None,
               is_active=None):
        """
        Updates user profile in the database with the specified parameters.\n
        :param first_name: first name of a user
        :type first_name: str
        :param middle_name: middle name of a user
        :type middle_name: str
        :param last_name: last name of a user
        :type last_name: str
        :param password: password of a user
        :type password: str
        :param role: role id
        :type role: int
        :param is_active: activation state
        :type is_active: bool
        :return: None
        """
        try:
            valid_bio_info(first_name, last_name, middle_name)

            if first_name:
                self.first_name = first_name

            if last_name:
                self.last_name = last_name

            if middle_name:
                self.middle_name = middle_name

            if password:
                validate_password(password)
                self.set_password(password)

            if role:
                self.role = role

            if is_active:
                self.is_active = is_active

            self.save()
        
        except ValidationError:
            raise

        else:
            return self


    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all users
        """
        return CustomUser.objects.all()


    def get_role_name(self):
        """
        returns str role name
        """
        return ROLE_CHOICES[self.role][1]
