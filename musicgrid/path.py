from .main import App
from . import model, collection


@App.path(model=model.Root, path='')
def get_document():
   return model.Root()

@App.path(model=collection.UserCollection, path='users')
def get_user_collection():
    return collection.UserCollection()
