from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms


class UserRegisterForm(ModelForm):
    # confirm_password = forms.CharField( widget=forms.PasswordInput(
    #   attrs={'class': 'form-control', 'placeholder': 'Şifre Tekrarı'}))
    # email = forms.CharField(help_text=("Enter the same password as before, for verification."))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'input-text', 'name': 'name', 'id': 'name', 'type': 'text',
                       'value': '',
                       'required': 'required'}),
            'last_name': forms.TextInput(
                attrs={'class': 'input-text', 'name': 'lastname', 'id': 'lastname',
                       'required': 'required'}),

            'email': forms.TextInput(
                attrs={'class': 'input-text', 'name': 'email', 'id': 'email2',
                       'required': 'required'}),
            'password': forms.PasswordInput(
                attrs={'class': 'input-text ', 'name': 'password1', 'id': 'password1'}),


        }

        # User._meta.get_field_by_name('email').unique = True
        User._meta.get_field('email')._unique = True

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")
        return data
