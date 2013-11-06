from StringIO import StringIO

from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory

from us_ignite.common import csv_unicode as csv
from us_ignite.profiles.models import Profile, ProfileLink


class UserRegistrationForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(
        widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(
        widget=forms.PasswordInput(), label="Repeat your password")

    def clean_email(self):
        """Makes sure this email is unique"""
        if 'email' in self.cleaned_data:
            try:
                User.objects.get(email__iexact=self.cleaned_data['email'])
            except User.DoesNotExist:
                return self.cleaned_data['email']
            else:
                raise forms.ValidationError(
                    'This email has already been registered')

    def clean(self):
        """Make sure the passwords are equal."""
        cleaned_data = self.cleaned_data
        if cleaned_data.get('password1') and cleaned_data.get('password2'):
            if not cleaned_data['password1'] == cleaned_data['password2']:
                raise forms.ValidationError('Passwords are not the same')
            return cleaned_data
        raise forms.ValidationError('Passwords are required.')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('name', 'website', 'bio')


ProfileLinkFormSet = inlineformset_factory(
    Profile, ProfileLink, max_num=3, extra=1)


class InviterForm(forms.Form):
    users = forms.CharField(widget=forms.Textarea,
                            help_text='Users must be in a ``name, email`` '
                            'format each new user must be in a new line.')

    def _validate_user(self, row):
        try:
            # Unpack the row
            name, email = row
        except (ValueError, TypeError):
            raise forms.ValidationError(
                '``%s`` has an invalid format. Must be ``name, email``'
                % ','.join(row))
        # Remove email whitespace:
        email = email.replace(' ', '')
        try:
            validators.validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError('Invalid email: ``%s``' % email)
        return (name, email)

    def clean_users(self):
        """Prepares the users to be imported.

        The output will be a list of tuples of name and email address::

            [('Name', 'Email address')]
        """
        if self.cleaned_data.get('users'):
            users_csv = csv.UnicodeReader(
                StringIO(self.cleaned_data.get('users')))
            cleaned_users = []
            for row in users_csv:
                if not row:
                    continue
                user_row = self._validate_user(row)
                if user_row:
                    cleaned_users.append(user_row)
            return cleaned_users
