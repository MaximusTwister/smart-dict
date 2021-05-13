from django import forms
from .models import WordCard, Dictionary


class DictForm(forms.ModelForm):
    class Meta:
        model = Dictionary
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CardForm(forms.ModelForm):
    class Meta:
        model = WordCard
        fields = ['word_foreign', 'word_native', 'context_foreign', 'context_native']


class NewCardForm(forms.ModelForm):
    class Meta:
        model = WordCard
        fields = ['word_foreign', 'word_native', 'context_foreign', 'context_native']
        widgets = {
            'word_foreign': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'word_native': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'context_foreign': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'context_native': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }