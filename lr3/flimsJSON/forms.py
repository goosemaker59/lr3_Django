from django import forms

class FilmsForm(forms.Form):
    title = forms.CharField(max_length=100, label="Название фильма")
    gerne = forms.CharField(max_length=30, label="Жанр")
    director = forms.CharField(max_length= 100, label="Режиссёр")
