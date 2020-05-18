from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms


class UserForm(ModelForm):
    # confirm_password = forms.CharField( widget=forms.PasswordInput(
    #   attrs={'class': 'form-control', 'placeholder': 'Şifre Tekrarı'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Ad', 'required': 'required'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': ' Soyad', 'required': 'required'}),
            'username': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Kullanıcı Adı'}),
            'email': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'E-mail', 'required': 'required'}),

        }

        # CustomerCompany._meta.get_field_by_name('email').unique = True
        User._meta.get_field('email')._unique = True

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")
        return data
