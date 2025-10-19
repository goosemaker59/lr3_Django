from django.shortcuts import render, redirect
from .forms import FilmsForm, FileForm
from django.conf import settings
from datetime import datetime
import os
import json
import uuid

def index(request):
    response = render(request, "index.html", {})
    return response
def film_list(request):
    if request.method == 'POST':
        file_form = FileForm(request.POST, request.FILES)
        if file_form.is_valid():
            title = file_form.cleaned_data['title']
            uploaded_file = file_form.cleaned_data['file']

            ext = os.path.splitext(uploaded_file.name)[1]  # Генерируем уникальное имя
            unique_name = f"{uuid.uuid4()}{ext}"
            file_path = os.path.join(settings.MEDIA_ROOT, unique_name)
            # Сохраняем файл
            with open(file_path, 'wb+') as dest:
                for chunk in uploaded_file.chunks():
                    dest.write(chunk)
                    # Сохраняем метаданные в JSON
            save_file_metadata(
                filename=unique_name,
                original_name=uploaded_file.name,
                title=title,
                size=uploaded_file.size
            )
            return redirect('film_list')
    else:
        file_form = FileForm()


    films = get_file_metadata()
    response = render(request, "film_list.html", {
        "file_form": file_form,
        "films": films
    })
    return response
def film_add(request):
    if request.method == 'POST':
        films_form = FilmsForm(request.POST)
        if films_form.is_valid():
            save_film_data(films_form.cleaned_data)
    else:
        films_form = FilmsForm()
    response = render(request, "film_add.html", {
        "films_form": films_form
    })
    return response
def save_film_data(data):
    folder_path = os.path.join(settings.BASE_DIR, 'Films')
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, 'films.json')
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)

    with open(file_path, 'r+') as f:
        films = json.load(f)
        films.append(data)
        f.seek(0)
        json.dump(films, f, ensure_ascii=False, indent=4)


def save_file_metadata(filename, original_name, title, size):
    metadata_file = os.path.join(settings.MEDIA_ROOT, 'file_metadata.json')
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    else:
        metadata = []

        metadata.append({
            'id': len(metadata) + 1,
            'filename': filename,
            'original_name': original_name,
            'title': title,
            'size': size,
            'upload_date': datetime.now().isoformat()
        })
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

def get_file_metadata():
    metadata_file = os.path.join(settings.MEDIA_ROOT, 'file_metadata.json')
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

