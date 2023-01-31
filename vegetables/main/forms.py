from .models import User, Crop
from django import forms
from .choices import KIND, AMOUNT
from phonenumber_field.modelfields import PhoneNumberField


class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label="First name", max_length=20, widget=forms.TextInput(attrs={'class': 'cell'}))
    last_name = forms.CharField(label="Last name", max_length=20, widget=forms.TextInput(attrs={'class': 'cell'}))
    email = forms.EmailField(label="Email address", widget=forms.EmailInput(attrs={'class': 'cell'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'cell'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'cell'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email=cd['email']):
            raise forms.ValidationError('Account with this email already exists.')
        return cd['email']


class UserLoginForm(forms.ModelForm):
    email = forms.EmailField(label="Login", widget=forms.TextInput(attrs={'class': 'cell'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'cell'}))

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean_password(self):
        cd = self.cleaned_data
        user = User.objects.filter(email=cd['email']).values()
        try:
            for i in range(0, user.count()):
                if user[i]['password'] == cd['password'] and cd['email'] == user[i]['email']:
                    return cd['password']
            else:
                raise forms.ValidationError('Incorrect password')
        except KeyError:
            raise forms.ValidationError('Incorrect login or password')


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(label="First name", max_length=20, required=False,
                                 widget=forms.TextInput(attrs={'class': 'cell'}))
    last_name = forms.CharField(label="Last name", max_length=20, required=False,
                                widget=forms.TextInput(attrs={'class': 'cell'}))
    email = forms.EmailField(label="Email address", required=False, initial='',
                             widget=forms.TextInput(attrs={'class': 'cell'}))
    # phone = PhoneNumberField("Phone", required=False)
    city = forms.CharField(label="City", max_length=20, required=False,
                           widget=forms.TextInput(attrs={'class': 'cell'}))
    address = forms.CharField(label="Address", max_length=20, required=False,
                              widget=forms.TextInput(attrs={'class': 'cell'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'cell'}), required=False)
    image = forms.ImageField(label='You image', required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'city', 'address', 'password', 'image')

    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email=cd['email']):
            raise forms.ValidationError('Account with this email already exists.', code='email')
        return cd['email']


class CropNewForm(forms.ModelForm):
    name = forms.CharField(label="Product", max_length=20, widget=forms.TextInput(attrs={'class': 'cell'}))
    amount = forms.ChoiceField(label="Amount", choices=AMOUNT, widget=forms.Select(attrs={'class': 'cell'}))
    kind = forms.ChoiceField(label="Kind", choices=KIND, widget=forms.Select(attrs={'class': 'cell'}))
    price = forms.FloatField(label="Price", widget=forms.NumberInput(attrs={'class': 'cell'}))
    image = forms.ImageField(label='You image', required=False)

    class Meta:
        model = Crop
        fields = ('name', 'amount', 'kind', 'price', 'image')


class CropEditForm(forms.ModelForm):
    name = forms.CharField(label="Product", max_length=20, widget=forms.TextInput(attrs={'class': 'cell'}))
    amount = forms.ChoiceField(label="Amount", choices=AMOUNT, widget=forms.Select(attrs={'class': 'cell'}))
    kind = forms.ChoiceField(label="Kind", choices=KIND, widget=forms.Select(attrs={'class': 'cell'}))
    price = forms.FloatField(label="Price", widget=forms.NumberInput(attrs={'class': 'cell'}))
    image = forms.ImageField(label='You image', required=False)

    class Meta:
        model = Crop
        fields = ('name', 'amount', 'kind', 'price', 'image')
