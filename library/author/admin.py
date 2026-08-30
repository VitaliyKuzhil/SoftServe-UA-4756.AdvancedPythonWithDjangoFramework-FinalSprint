from django.contrib import admin
from author.models import Author



@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    empty_value_display = '-empty-'

    list_display = ['pretty_author_information', 'name', 'surname', 'patronymic', 'count_of_books', 'get_books']

    search_fields = ['name', 'books__name']
    list_filter = ['id', 'name', 'surname', 'patronymic']
    list_editable = []

    filter_horizontal = ['books']

    fieldsets = [
        ('About Author', {
            'fields': [('surname', 'name', 'patronymic')],
            'description': 'Grate writer'
        }),
        ('Author\'s Books', {
            'fields': ['books']
        })
    ]

    readonly_fields = []


    @admin.display(description='author')
    def pretty_author_information(self, obj):

        if obj.id:
            return f'Author № {obj.id}'

        return None


    @admin.display(description='books')
    def get_books(self, obj):

        if obj.books.exists():
            return ' | '.join(f'{book.name}' for book in obj.books.all())

        return 'Eny written books, yet'


    @admin.display(description='count of books')
    def count_of_books(self, obj):
        return obj.books.count()
