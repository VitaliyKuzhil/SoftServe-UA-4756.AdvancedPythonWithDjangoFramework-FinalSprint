from django.contrib import admin
from book.models import Book
from author.models import Author



class AuthorInline(admin.TabularInline):
    model = Author.books.through
    extra = 1
    verbose_name = 'Author of this book'
    verbose_name_plural = 'Authors of this book'



@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['pretty_book_information', 'name', 
                    'get_authors', 'description', 
                    'count', 'get_units_in_orders']

    search_fields = ['name', 'authors__name']
    list_filter = ['id', 'name', 'authors']

    
    fieldsets = [
        ('About Book', {
            'fields': [('name', 'description', 'count')],
            'description': 'Grate book'
        })
    ]

    inlines = [AuthorInline]

    readonly_fields = []


    @admin.display(description='id')
    def pretty_book_information(self, obj):

        if obj.id:

            return f'Book № {obj.id}'

        return None


    @admin.display(description='authors')
    def get_authors(self, obj):

        if obj.authors.exists():

            return ' | '.join(f'{author.name} {author.patronymic} {author.surname}' for author in obj.authors.all())

        return 'Unknown author'


    @admin.display(description='units in orders')
    def get_units_in_orders(self, obj):

        if obj.book_orders.exists():

            return obj.book_orders.count()
        
        return 'Not borrowed, yet'
