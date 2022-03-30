
from django import forms
from pythonbasic.models import CommentPython



class CommentForm(forms.ModelForm):

    class Meta:
        model = CommentPython
        fields = ('author', 'email', 'body')
        widgets = {
            'author':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'email':forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}),
            'body':forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Commentaire ...'}),
        }
   

