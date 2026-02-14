# myapp/forms.py
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body'] # Specify which fields to include
        # Alternatively, use fields = '__all__' to include all fields
        # or exclude = ['field_name'] to exclude specific fields
