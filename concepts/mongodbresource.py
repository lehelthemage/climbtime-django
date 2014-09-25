# coding: utf-8

from bson import ObjectId

from tastypie.bundle import Bundle
from tastypie.resources import Resource
from django.core.exceptions import ObjectDoesNotExist
from django.http import QueryDict
from pymongo import Connection
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


db = Connection(
    host=getattr(settings, "MONGODB_HOST", None),
    port=getattr(settings, "MONGODB_PORT", None)
)[settings.MONGODB_DATABASE]



class MongoDBResource(Resource):
    """
    A base resource that allows to make CRUD operations for mongodb.
    """


    def get_object_class(self):
        return self._meta.object_class

    def get_collection(self):
        try:
            return db[self._meta.collection]
        except AttributeError:
            raise ImproperlyConfigured("Define a collection in your resource.")

    def apply_filters(self, request, applicable_filters):
        return list(map(self.get_object_class(), self.get_collection().find(applicable_filters)))

    def build_filters(self, filters):
        if isinstance(filters, QueryDict):
            return filters.dict()

        return filters

    def get_object_list(self, request):
        bundle = self.build_bundle(request=request)
        return self.obj_get_list(bundle)

    def obj_get_list(self, bundle, **kwargs):
        """
        Maps mongodb documents to resource's object class.
        """

        filters = {}
        result = []

        self.authorized_read_list(result, bundle)

        if hasattr(bundle.request, 'GET'):
            filters = bundle.request.GET.copy()

        # Update with the provided kwargs.
        filters.update(kwargs)

        applicable_filters = self.build_filters(filters=filters)

        return self.apply_filters(bundle.request, applicable_filters)

    def obj_get(self, bundle, **kwargs):
        """
        Returns mongodb document from provided id.
        """

        obj = self.get_collection().find_one({
            "_id": ObjectId(kwargs.get("pk"))
        })

        if not obj:
            raise ObjectDoesNotExist

        self.authorized_read_detail(obj, bundle)

        return self.get_object_class()(obj)

    def obj_create(self, bundle, **kwargs):
        """
        Creates mongodb document from POST data.
        """

        bundle.data.update(kwargs)

        self.authorized_create_detail(bundle.data, bundle)

        oid = self.get_collection().insert(bundle.data)
        obj = self._meta.object_class.objects.get(_id=ObjectId(oid))

        return self.build_bundle(request=bundle.request, data=bundle.data, obj=obj)

    def obj_update(self, bundle, **kwargs):
        """
        Updates mongodb document.
        """

        self.authorized_update_detail(bundle.data, bundle)
        self.get_collection().update(
            {"_id": ObjectId(kwargs.get("pk"))},
            {"$set": bundle.data}
        )

        return bundle

    def obj_delete(self, bundle, **kwargs):
        """
        Removes single document from collection
        """

        parameters = {"_id": ObjectId(kwargs.get("pk"))}

        self.authorized_delete_detail(parameters, bundle)
        self.get_collection().remove(parameters)

    def obj_delete_list(self, bundle, **kwargs):
        """
        Removes all documents from collection
        """

        self.authorized_delete_list(bundle.data, bundle)
        self.get_collection().remove()

    def detail_uri_kwargs(self, bundle_or_obj):
        """
        Given a ``Bundle`` or an object, it returns the extra kwargs needed
        to generate a detail URI.

        By default, it uses the model's ``pk`` in order to create the URI.
        """

        detail_uri_name = getattr(self._meta, 'detail_uri_name', 'pk')
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            if isinstance(bundle_or_obj.obj, ObjectId):
                kwargs[detail_uri_name] = str(bundle_or_obj.obj)
            else:
                kwargs[detail_uri_name] = getattr(bundle_or_obj.obj, detail_uri_name)
        else:
            kwargs[detail_uri_name] = getattr(bundle_or_obj, detail_uri_name)

        return kwargs