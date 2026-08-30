from django.contrib import admin
from authentication.models import CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    empty_value_display = '-empty-'

    list_display = [
        'pretty_user_information', 'first_name', 'last_name', 'middle_name', 
        'get_user_orders', 'email', 'role', 'is_superuser', 'is_active', 
        'created_at','updated_at'
    ]
    
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['role', 'is_active', 'created_at']
    list_editable = []
    
    fields = [
        ('first_name', 'last_name', 'middle_name'), 
        'email', ('role', 'is_superuser', 'is_active'), 
        'created_at','updated_at'
        ]
    readonly_fields = ['created_at','updated_at']


    @admin.display(description='id')
    def pretty_user_information(self, obj):
        if obj.id:
            return f'User {obj.id}'
        return None


    @admin.display(description='orders')
    def get_user_orders(self, obj):

        if obj.user_orders.exists():

            return obj.user_orders.count()
        
        return 'No orders, yet'
    