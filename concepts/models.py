from mongoengine import *
from mongoengine.django.auth import User
import datetime

PROPERTY_TYPE = (    ('Num', 'Number'),
                     ('TF', 'True/False'),
                     ('Str', 'String'),
                     ('Date', 'Date & Time'),
                     ('Days', 'Day(s) of Week'),
                     ('Time', 'Time'),
                     ('Dur', 'Time Duration'),
                     ('Url', 'URL'),
                     ('Geo', 'Location'),
                     ('Con', 'Topic'))


class Picture(Document):
    id = ObjectIdField(primary_key=True)
    caption = StringField(max_length=400, default='')
    image = ImageField()

    def __unicode__(self):
        return str(self.id)


class Feature(Document):
    id = ObjectIdField(primary_key=True)
    title = StringField(max_length=100, required=True)
    is_property = BooleanField(default=True)
    property_type = StringField(max_length=50, choices=PROPERTY_TYPE)

    def __unicode__(self):
        return self.title or u''


class Category(Document):
    id = ObjectIdField(primary_key=True)
    author = ReferenceField(User, required=True)
    title = StringField(max_length=200, required=True)
    description = StringField(max_length=2000, required=True)
    version = IntField(default=1)
    ancestors = ListField(ReferenceField('self'))
    ancestor_associations = ListField(IntField())
    parent = ReferenceField('self', default=None)
    features = ListField(ReferenceField(Feature))
    pictures = ListField(ReferenceField(Picture))
    default_picture = ReferenceField(Picture)
    date_modified = DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.title


class CategoryAssociation(EmbeddedDocument):
    up_votes = IntField(default=1)
    down_votes = IntField(default=1)
    category = ReferenceField(Category, required=True)

    def __unicode__(self):
        return self.category


class Property(EmbeddedDocument):
    property_id = ObjectIdField(unique=True, primary_key=True)
    feature = ReferenceField(Feature)
    value = StringField(max_length=2000, required=True)

    def __unicode__(self):
        return unicode(self.feature)


class Concept(Document):
    id = ObjectIdField(primary_key=True)
    title = StringField(max_length=200, required=True)
    version = IntField(default=1)
    original_version_id = ObjectIdField()
    description = StringField(max_length=2000, default='')
    author = ReferenceField(User, required=True)
    pub_date = DateTimeField(help_text='date published', required=True)
    pictures = ListField(ReferenceField(Picture))
    default_picture = ReferenceField(Picture)
    categories = ListField(EmbeddedDocumentField(CategoryAssociation))
    properties = ListField(EmbeddedDocumentField(Property))
    date_modified = DateTimeField(default=datetime.datetime.now)


def __unicode__(self):
    return self.title or u''




