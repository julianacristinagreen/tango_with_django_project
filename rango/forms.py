from django import forms
from rango.models import Page, Category
from django.contrib.auth.models import User
from rango.models import UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category._meta.get_field('name').max_length, help_text="Please enter the category name.")
    #users wont be able to enter a value for this field.
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    #users wont be able to enter a value for this field.
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    #users wont be able to enter a value for this field.
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model.
        #Django creates a form in the specified imae of the specified model.
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page._meta.get_field('title').max_length, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    #users wont be able to enter a value for this field.
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        #Django creates a form in the specified imae of the specified model.
        model  =Page

        #To customise what you want in your form, we can
        #exclude the caregory field from the form,
        exclude = ('category', )
        #or specifiy the fields to include
        #fields = ('title', 'url', 'views')

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with 'http://',
        # then prepend 'http://'.
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)