# concepts/api.py
from tastypie.resources import ModelResource
from concepts.models import Concept, Category

from mongodbresource import MongoDBResource


class ConceptResource(MongoDBResource):
    class Meta:
        queryset = Concept.objects.all()
        resource_name = 'concept'


class CategoryResource(MongoDBResource):
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'
        collection = 'category'
    def get_resource_uri(self, bundle_or_obj=None):
        super(MongoDBResource, self).get_resource_uri(self, bundle_or_obj)

