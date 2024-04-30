from django import forms
from .models import Room

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model =Room
        fields=['name','img_question'] 
        labels ={
            'name': 'Subject Of Question', 
            'img_question': 'Picture of the problem',
        }