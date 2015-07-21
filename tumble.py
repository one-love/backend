from mongoengine import *


connect('tumbleblog')


class User(Document):
    """
    Tumble Log User
    """
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)


class Post(Document):
    """
    Tumble Log Post
    """
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)

    meta = {
        'allow_inheritance': True,
    }


class TextPost(Document):
    """
    Tumble Log TextPost
    """
    content = StringField()


class ImagePost(Post):
    """
    Tumble Log ImagePost
    """
    image_path = StringField()


class LinkPost(Post):
    """
    Tumble Log LinkPost
    """
    link_url = StringField()
