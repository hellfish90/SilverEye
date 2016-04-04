
from Utils.collection_manager import Extractor
from pymongo import MongoClient
from django.shortcuts import render
from django.shortcuts import redirect

server = '127.0.0.1'

port = 27017

from .forms import TagsForm, CollectionsForm

def list_collections(request):
    client = MongoClient(server, port, connect=True)
    collection_manager = Extractor(client)

    collections = collection_manager.get_all_collections()

    return render(request, 'list_collections.html', {'collections': collections})


def add_tag_to_collection(request):

    client = MongoClient(server, port, connect=True)
    collection_manager = Extractor(client)

    collections = collection_manager.get_all_collections()

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TagsForm(request.POST, choices=collections)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

            print form.data['collection']

            collection_manager.add_tag_to_collection(form.data['collection'], form.data['name'])

            return redirect('/query/collections/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TagsForm(choices=collections)

    return render(request, 'tag_form.html', {'form': form})


def add_collection(request):

    client = MongoClient(server, port, connect=True)
    collection_manager = Extractor(client)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CollectionsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

            collection_manager.add_collection(form.data['name'])

            return redirect('/query/collections/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CollectionsForm()

    return render(request, 'collection_form.html', {'form': form})


def remove_collection(request, id):

    client = MongoClient(server, port, connect=True)
    collection_manager = Extractor(client)
    collection_manager.remove_collection(id)

    return redirect('/query/collections/')

def remove_tag(request, collection, tag):

    client = MongoClient(server, port, connect=True)
    collection_manager = Extractor(client)

    print collection
    print tag

    collection_manager.delete_tag_to_collection(collection, tag)

    return redirect('/query/collections/')