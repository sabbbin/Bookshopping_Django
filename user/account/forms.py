from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from .models import USERNAME_REGEX
User=get_user_model()

class userloginform(forms.Form):
    username=forms.CharField(label='username')

    password=forms.CharField(label='password', widget=forms.PasswordInput)

    def clean(self,*args,**kwargs):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')

        user_qs=User.objects.filter(username=username).first()
        if not user_qs:
            raise forms.ValidationError("invalid credatials")
        else:
            if not user_qs.check_password(password):
                raise forms.ValidationError('invalid credatials')
        super(userloginform,self).clean(*args,**kwargs)    



class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
   
    class Meta:
        model = User
        fields = ('email','image', 'username','lastname','firstname','rollno','grade')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        print(user.image)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'is_active', 'is_admin','image')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]