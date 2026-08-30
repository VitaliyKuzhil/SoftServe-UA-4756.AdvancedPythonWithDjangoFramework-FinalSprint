from django import forms
from django.utils import timezone
from book.models import Book
from django.core.validators import MinValueValidator, MaxValueValidator
from authentication.constants import MIN_AMOUNT_OF_BOOK, MAX_AMOUNT_OF_BOOK
from order.constants import LOAN_PERIOD
from order.models import Order



class CreateAnOrderForm(forms.ModelForm):

    book = forms.ModelChoiceField(required=True, queryset=Book.objects.all(), initial=1, label='Book', 
                                  empty_label=None, widget=forms.Select(attrs={'class': 'form-select'}))
    copies = forms.IntegerField(required=False, label='Copies', initial=MIN_AMOUNT_OF_BOOK,
                                   validators=[MinValueValidator(MIN_AMOUNT_OF_BOOK, message=f'The count couldn\'t be fewer than {MIN_AMOUNT_OF_BOOK}'),
                                               MaxValueValidator(MAX_AMOUNT_OF_BOOK, message=f'The count couldn\'t be bigger than {MAX_AMOUNT_OF_BOOK}')],
                                   widget=forms.NumberInput(attrs={
                                       'class': 'form-control', 'min': str(MIN_AMOUNT_OF_BOOK), 'max': str(MAX_AMOUNT_OF_BOOK), 
                                       'placeholder': 'Write the number of units you\'re want to borrow'}))



    class Meta:
        model = Order
        fields = ['book', 'copies']


    def __init__(self,*args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        self.fields['book'].label_from_instance = lambda obj: f'{obj.name} (Available: {obj.count})'


    def clean(self):
        cleaned_data = super().clean()
        
        selected_book = cleaned_data.get('book')
        requested_copies = cleaned_data.get('copies')

        if selected_book and requested_copies:
            
            available_copies = selected_book.count 

            if available_copies < requested_copies:
                raise forms.ValidationError(f'There are only {available_copies} copies of this book available.')

        return cleaned_data


    def save(self, commit=True):
        order = super().save(commit=False)
        
        if self.request:
            order.user = self.request.user

        order.plated_end_at = timezone.now() + LOAN_PERIOD

        selected_book = self.cleaned_data.get('book')
        requested_copies = self.cleaned_data.get('copies', 1)

        selected_book.count -= requested_copies
        selected_book.save()

        order.copies = requested_copies

        if commit:
            order.save()

        return order
