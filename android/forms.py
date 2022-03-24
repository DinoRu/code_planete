from django import forms
from android.models import CommentArticle


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentArticle
        fields = ('author', 'email', 'body')
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom:'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Nom:'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Commentaire ....'})
        }

    
