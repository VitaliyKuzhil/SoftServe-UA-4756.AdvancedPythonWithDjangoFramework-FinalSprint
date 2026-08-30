from django import forms
from author.models import Author
from authentication.constants import MAX_NAME_CHARACTERS


class CreateAnAuthorForm(forms.ModelForm):

    name = forms.CharField(required=True, max_length=MAX_NAME_CHARACTERS, label="Name",
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write name here'}))
    surname = forms.CharField(required=True, max_length=MAX_NAME_CHARACTERS, label="Surname",
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write surname here'}))
    patronymic = forms.CharField(required=True, max_length=MAX_NAME_CHARACTERS, label="Patronymic",
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write patronymic here'}))
    
    class Meta:
        model = Author
        fields = ('name', 'surname', 'patronymic')


    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name', '').strip()
        surname = cleaned_data.get('surname', '').strip()
        patronymic = cleaned_data.get('patronymic', '').strip()

        if name and surname and patronymic:
            author_exists = Author.objects.filter( name__iexact=name, surname__iexact=surname, patronymic__iexact=patronymic).exists()

            if author_exists:
                raise forms.ValidationError("This author is already exists.")

        return cleaned_data



class UpdateAnAuthorForm(forms.ModelForm):

    name = forms.CharField(required=True, max_length=MAX_NAME_CHARACTERS, label="Name",
                                     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write name here'}))
    surname = forms.CharField(required=True, max_length=MAX_NAME_CHARACTERS, label="Surname",
                                     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write surname here'}))
    patronymic = forms.CharField(required=True, max_length=MAX_NAME_CHARACTERS, label="Patronymic",
                                     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write patronymic here'}))
        
    class Meta:
        model = Author
        fields = ('name', 'surname', 'patronymic')
