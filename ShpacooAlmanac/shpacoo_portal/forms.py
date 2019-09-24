from django import forms


class UserCreateForm(forms.Form):
    username = forms.CharField(label='Login', max_length=128)
    email = forms.CharField(label='E-mail', max_length=128)
    password = forms.CharField(label='Hasło', max_length=128, widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.CharField(label='Login', max_length=128)
    password = forms.CharField(label='Hasło', max_length=128, widget=forms.PasswordInput)


class AddArtistForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter new artist...'}))
