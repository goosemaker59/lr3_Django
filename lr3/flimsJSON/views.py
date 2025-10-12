from django.shortcuts import render
from .forms import FilmsForm
import os
import json

def index(request):

    response = render(request, "index.html", {

     })

    return response

def film_list(request):

    response = render(request, "film_list.html", {
     })

    return response

def film_add(request):
    films_form = FilmsForm()
    response = render(request, "film_add.html", {
        "films_form": films_form
    })

    return response
