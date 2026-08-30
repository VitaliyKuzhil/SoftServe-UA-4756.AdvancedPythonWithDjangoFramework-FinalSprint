from django.contrib import admin
from order.models import Order



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ['pretty_order_information', 'pretty_book_information', 'pretty_user_information', 'is_active', 
                    'created_at', 'plated_end_at', 'end_at']
    
    search_fields = ['book__name', 'user__email']

    list_filter = ['created_at', 'plated_end_at', 'end_at']

    list_editable = []

    fieldsets = [
        ('Static Data', {
            'fields': ['book', 'user'],
            'description': 'Main order data(book and user)'
        }),
        ('Changed Data', {
            'fields': ['is_active', ('created_at', 'plated_end_at', 'end_at')],
            'description': 'Additional data which chances(order status and date fields)'
        }),
    ]

    readonly_fields = ['book', 'user', 'created_at', 'end_at']


    @admin.display(description='id')
    def pretty_order_information(self, obj):

        if obj.id:

            return f'Order № {obj.id}'
        
        return None


    @admin.display(description='book')
    def pretty_book_information(self, obj):

        if obj.book:

            return f'ID: {obj.book.id}, Name: {obj.book.name}'
        
        return None


    @admin.display(description='user')
    def pretty_user_information(self, obj):

        if obj.user:

            return f'Name: {obj.user.first_name}, Email: {obj.user.email}'
        
        return None
