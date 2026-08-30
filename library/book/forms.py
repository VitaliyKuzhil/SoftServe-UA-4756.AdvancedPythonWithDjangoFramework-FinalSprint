from django import forms
from book.models import Book
from django.core.validators import MinValueValidator
from authentication.constants import MAX_BOOK_NAME, MAX_BOOK_DESCRIPTION, DEFAULT_NUMBER_OF_BOOKS
from author.models import Author



class CreateABookForm(forms.ModelForm):
    name = forms.CharField(required=True, max_length=MAX_BOOK_NAME, label='Name',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write name of a book here'}))
    description = forms.CharField(required=False, max_length=MAX_BOOK_DESCRIPTION, label='Description',
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'row': '3',
                                                               'placeholder': 'Write description of a book here'}))
    count = forms.IntegerField(required=False, label='Count', initial=DEFAULT_NUMBER_OF_BOOKS,
                               validators=[MinValueValidator(1, message='The count couldn\'t be fewer than 1')],
                               widget=forms.NumberInput(attrs={
                                   'class': 'form-control', 'min': '1', 'placeholder': 'Write the number of units'}))
    authors = forms.ModelMultipleChoiceField(required=False, queryset=Author.objects.all(), label='Book\'s Authors', 
                                             widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'authors']


    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
    
            self.fields['authors'].label_from_instance = lambda obj: f'{obj.name} {obj.surname} {obj.patronymic}'


    def save(self, commit=True):
        book = super().save(commit=commit)

        if commit:
            selected_authors = self.cleaned_data.get('authors')
            
            for author in selected_authors:
                author.books.add(book)

        return book



class UpdateABookForm(forms.ModelForm):
    name = forms.CharField(required=True, max_length=MAX_BOOK_NAME, label='Name',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write name of a book here'}))
    description = forms.CharField(required=False, max_length=MAX_BOOK_DESCRIPTION, label='Description',
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'row': '3',
                                                               'placeholder': 'Write description of a book here'}))
    count = forms.IntegerField(required=False, label='Count', initial=DEFAULT_NUMBER_OF_BOOKS,
                               validators=[MinValueValidator(1, message='The count couldn\'t be fewer than 1')],
                               widget=forms.NumberInput(attrs={
                                   'class': 'form-control', 'min': '1', 'placeholder': 'Write the number of units'}))
    authors = forms.ModelMultipleChoiceField(required=False, queryset=Author.objects.all(), label='Book\'s Authors', 
                                             widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'authors']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            if hasattr(self.instance, 'authors'):
                self.fields['authors'].initial = self.instance.authors.all()
            else:
                self.fields['authors'].initial = Author.objects.filter(books=self.instance)


    def save(self, commit=True):
        book = super().save(commit=commit)

        if commit:
            selected_authors = self.cleaned_data.get('authors')
            
            if hasattr(book, 'authors'):
                book.authors.clear()
            else:
                for author in Author.objects.filter(books=book):
                    author.books.remove(book)

            for author in selected_authors:
                author.books.add(book)

        return book

