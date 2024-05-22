from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from models import Product



class CustomUserCreationForm(forms.Form):
    name = forms.CharField(max_length=30, label='Name')
    firstname = forms.CharField(max_length=30, label='Firstame')
    email = forms.EmailField(max_length=254, label='Email')
    picture = forms.ImageField(label='Profile Picture', required=False)
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )


class ConnectionForm(forms.Form):
    email = forms.EmailField(max_length=254, label='Email')
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

class AdminCreationForm(forms.Form):
    pseudo = forms.CharField(max_length=30, label='Name')
    email = forms.EmailField(max_length=254, label='Email')
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )    

class AddProductForm(forms.Form):
    identifier = forms.CharField(max_length=79, label='Identifier')
    description = forms.CharField(max_length=125, label='Description')
    price = forms.IntegerField(label='Price')
    picture = forms.ImageField(label='Product Picture', required=False)
    stock = forms.IntegerField(label = 'Stock')

    
class UpdateProductForm(forms.Form):
    # id = forms.IntegerField(label='Id')
    identifier = forms.CharField(max_length=79, label='Identifier')
    description = forms.CharField(max_length=125, label='Description')
    price = forms.IntegerField(label='Price')
    picture = forms.ImageField(label='Product Picture', required=False)
    stock = forms.IntegerField(label = 'Stock')

    
class SelectProductForm(forms.Form):
    id = forms.IntegerField(label='Id')
    identifier = forms.CharField(max_length=79, label='Identifier')

class DeleteProductForm(forms.Form):
    id = forms.CharField(label='Id')
