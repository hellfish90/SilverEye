import os
import sys
sys.path.append( os.path.dirname(os.path.dirname(__file__)) )
from DAO.DAOCollectionTags import DAOTags
from Core.Config.configuration import Configuration
from django.shortcuts import redirect
from django.shortcuts import render
from Utils.generate_circle_collections_tags import generate_flare
from .forms import TagsForm, CollectionsForm
from Core import CollectionClassifierController


def get_dao_tags_collections():
    configuration = Configuration()
    client = configuration.get_client()
    database_name = configuration.get_database_name()
    return DAOTags(client, database_name)


def list_collections(request):

    collections = get_dao_tags_collections().get_all_collection()
    generate_flare()

    return render(request, 'list_collections.html', {'collections': collections})


def list_unclassified_tags(request):

    tags = get_dao_tags_collections().get_unclassified_tags()
    generate_flare()


    return render(request, 'list_unclassified_tags.html', {'unclassified_tags': tags})


def add_tag_to_collection(request):

    collections_set = get_dao_tags_collections().get_all_collection()

    collections = [a["_id"] for a in collections_set]


    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TagsForm(request.POST, choices=collections)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:


            get_dao_tags_collections().add_tag_to_collection(form.data['collection'], form.data['name'])

            return redirect('/query/collections/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TagsForm(choices=collections)

    return render(request, 'tag_form.html', {'form': form})


def add_collection(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CollectionsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

            get_dao_tags_collections().add_collection(form.data['name'])

            return redirect('/query/collections/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CollectionsForm()

    return render(request, 'collection_form.html', {'form': form})


def remove_collection(request, id):

    get_dao_tags_collections().remove_collection(id)

    return redirect('/query/collections/')


def remove_tag(request, collection, tag):

    get_dao_tags_collections().remove_tag_of_collection(collection, tag)

    return redirect('/query/collections/')