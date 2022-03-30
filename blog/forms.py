from ckeditor.widgets import CKEditorWidget
from django import forms

from blog.models import Comment, Subscribe


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'name'}), label='name')
    email = forms.EmailField(label='Email')
    to = forms.EmailField(label='Email')
    comments = forms.CharField(required=False,
                              widget=forms.Textarea, label='Comment')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'email':forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}),
            'body':forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Commentaire ...'}),
        }


class SearchForm(forms.Form):
    query = forms.CharField()


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = '__all__'


