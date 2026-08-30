from django import forms
from authentication.constants import MAX_PASSWORD_CHARACTERS, MIN_PASSWORD_CHARACTERS, ROLE_CHOICES, MAX_EMAIL_CHARACTERS, MAX_NAME_CHARACTERS
from django.core.validators import MinLengthValidator
from django.contrib.auth import authenticate, get_user_model


CustomUser = get_user_model()



class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True, max_length=MAX_EMAIL_CHARACTERS, label="Email address",
                             help_text='user@gmail.com',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Write your email address here'}))

    first_name = forms.CharField(max_length=MAX_NAME_CHARACTERS, label="First Name", help_text='John',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your first name here'}))
    last_name = forms.CharField(max_length=MAX_NAME_CHARACTERS, label="Last Name", help_text='Smit',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your last name here'}))
    middle_name = forms.CharField(max_length=MAX_NAME_CHARACTERS, label="Middle Name", help_text='Doe',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your middle name here'}))

    role = forms.TypedChoiceField(required=True, label='Role', choices=ROLE_CHOICES,
                               coerce=int, initial=0,
                               widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))

    password1 = forms.CharField(required=True, label="Password", help_text='Write password', max_length=MAX_PASSWORD_CHARACTERS,
                                validators=[MinLengthValidator(MIN_PASSWORD_CHARACTERS)],
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Write password here'}))
    password2 = forms.CharField(required=True, label="Repeat password", help_text='Password again', max_length=MAX_PASSWORD_CHARACTERS,
                                validators=[MinLengthValidator(MIN_PASSWORD_CHARACTERS)],
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Write password again'}))



    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'middle_name', 'role')


    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('The email is already used.')
        
        return email


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")

        return password2


    def save(self, commit=True):
        user = super().save(commit=False)

        user.is_active = True

        password = self.cleaned_data['password1']
        user.set_password(password)

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, label='Email address', help_text='Input your Email address',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Write your email address here'}))
    password = forms.CharField(required=True, label='Password', help_text='Input your password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Write password here'}))


    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get('email', '').strip()
        password = cleaned_data.get('password', '')

        if email and password:
            user = CustomUser.objects.filter(email=email).first()

            if user and not user.is_active:
                raise forms.ValidationError('Your account is blocked.')

            self.user = authenticate(self.request, email=email, password=password)

            if self.user is None:
                raise forms.ValidationError('Enter a correct email and password.')

        return cleaned_data



class UpdateCustomUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=MAX_NAME_CHARACTERS, label="First Name", help_text='John',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your first name here'}))
    last_name = forms.CharField(max_length=MAX_NAME_CHARACTERS, label="Last Name", help_text='Smit',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your last name here'}))
    middle_name = forms.CharField(max_length=MAX_NAME_CHARACTERS, label="Middle Name", help_text='Doe',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your middle name here'}))



    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'middle_name')
