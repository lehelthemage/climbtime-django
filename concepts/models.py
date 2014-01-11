from mongoengine import *
from mongoengine.django.auth import User

PROPERTY_TYPE = (    ('Num', 'Number'),
                     ('Str', 'String'),
                     ('Date', 'Date & Time'),
                     ('Time', 'Time'),
                     ('Dur', 'Time Duration'),
                     ('Url', 'URL'),
                     ('Geo', 'Location'))


class Picture(EmbeddedDocument):
    caption = StringField(max_length=400)
    image = BinaryField(required=True)

    def __unicode__(self):
        return self.image


class Feature(EmbeddedDocument):
    title = StringField(max_length=100, required=True)
    is_property = BooleanField(default=True)
    property_type = StringField(max_length=50, choices=PROPERTY_TYPE)

    def __unicode__(self):
        return self.title or u''


class Category(Document):
    title = StringField(max_length=200, required=True)
    version = IntField(default=1)
    ancestors = ListField(EmbeddedDocumentField('self'))
    ancestor_associations = ListField(IntField())
    parent = EmbeddedDocumentField('self')
    features = ListField(EmbeddedDocumentField(Feature))

    def __unicode__(self):
        return self.title


class CategoryAssociation(EmbeddedDocument):
    up_votes = IntField(default=1)
    down_votes = IntField(default=1)
    category = ReferenceField(Category, required=True)

    def __unicode__(self):
        return self.category


class Property(EmbeddedDocument):
    property_id = ObjectIdField(unique=True)
    feature = EmbeddedDocumentField(Feature)
    value = StringField(max_length=2000, required=True)

    def __unicode__(self):
        return unicode(self.feature)


class Concept(Document):
    title = StringField(max_length=200, required=True)
    version = IntField(default=1)
    original_version_id = ObjectIdField()
    description = StringField(max_length=2000, default='')
    author = ReferenceField(User, required=True)
    pub_date = DateTimeField(help_text='date published', required=True)
    pictures = ListField(EmbeddedDocumentField(Picture))
    default_picture = EmbeddedDocumentField(Picture)
    categories = ListField(EmbeddedDocumentField(CategoryAssociation))
    properties = ListField(EmbeddedDocumentField(Property))


def __unicode__(self):
    return self.title or u''




