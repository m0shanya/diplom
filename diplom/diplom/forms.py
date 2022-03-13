from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    username = forms.CharField(max_length=200)
    email = forms.EmailField()
    password = forms.CharField(
        min_length=6, widget=forms.PasswordInput()
    )
    password_repeat = forms.CharField(
        min_length=6, widget=forms.PasswordInput()
    )

    def clean_password_repeat(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_repeat']:
            raise forms.ValidationError('Passwords don\'t match.')
        return self.cleaned_data['password_repeat']
