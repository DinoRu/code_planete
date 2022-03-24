from django import forms
from java.models import CommentJava


class CommentForm(forms.ModelForm):

    class Meta:
        model = CommentJava
        fields = ('author', 'email', 'body')
        widgets = {
            'author':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'email':forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}),
            'body':forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Commentaire ...'}),
        }
