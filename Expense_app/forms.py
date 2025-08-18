from django import forms

from Expense_app.models import User,ExpenseModels,Settlement

class UserregisterForm(forms.ModelForm):

    class Meta:

        model =User

        fields =['username','first_name','last_name','email','password']


class LoginForm(forms.Form):

    username=forms.CharField(max_length=100)

    password=forms.CharField(max_length=100)


class ExpenseForm(forms.ModelForm):

    class Meta:

        model=ExpenseModels

        fields=['amount','description','bill_image']
        


class SettilmentForm(forms.ModelForm):

    class Meta:

        model=Settlement

        fields=['receiver_user','settle_amount']


class ForgotForm(forms.ModelForm):

    class Meta:

        model=User

        fields=['username']


class OtpForm(forms.Form):

    otp=forms.CharField(max_length=50)


class ResetPasswordForm(forms.Form):

    new_password=forms.CharField(max_length=50)

    confirm_password=forms.CharField(max_length=50)


class profileForm(forms.ModelForm):

    class Meta:

        model =User

        fields =['username','first_name','last_name','email']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            })},
    
    