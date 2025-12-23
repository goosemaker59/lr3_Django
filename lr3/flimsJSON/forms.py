from django import forms

class FilmsForm(forms.Form):
    title = forms.CharField(max_length=100, label="Название фильма")
    gerne = forms.CharField(max_length=30, label="Жанр")
    director = forms.CharField(max_length= 100, label="Режиссёр")
    country = forms.CharField(max_length=50, label="Страна производства")

class FileForm(forms.Form):
    title = forms.CharField(max_length=100, label="Название файла")
    file = forms.FileField(label="Импорт файла")

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.lower().endswith('.json'):
                raise forms.ValidationError("Разрешены только файлы с расширением .json.")
        return file
