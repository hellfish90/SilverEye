
from pymongo import MongoClient
from django.shortcuts import render
from django.shortcuts import redirect

from Utils.generate_circle_collections_tags import generate_flare
from Utils.collection_classifier import CollectionClassifier

from .forms import TagsForm, CollectionsForm

server = '127.0.0.1'

port = 27017


def list_collections(request):
    client = MongoClient(server, port, connect=True)
    collection_manager = CollectionClassifier(client)

    collections = collection_manager.get_all_collections()
    generate_flare()

    print collections

    return render(request, 'list_collections.html', {'collections': collections})


def list_unclassified_tags(request):
    client = MongoClient(server, port, connect=True)
    collection_manager = CollectionClassifier(client)

    tags = collection_manager.get_all_unclassified_tags()
    generate_flare()

    print tags

    return render(request, 'list_unclassified_tags.html', {'unclassified_tags': tags})


def add_tag_to_collection(request):

    client = MongoClient(server, port, connect=True)
    collection_manager = CollectionClassifier(client)

    collections = collection_manager.get_all_collection_names()
    print collections

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
    collection_manager = CollectionClassifier(client)

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
    collection_manager = CollectionClassifier(client)
    collection_manager.remove_collection(id)

    return redirect('/query/collections/')


def remove_tag(request, collection, tag):

    client = MongoClient(server, port, connect=True)
    collection_manager = CollectionClassifier(client)

    print collection
    print tag

    collection_manager.remove_tag_of_collection(collection, tag)

    return redirect('/query/collections/')