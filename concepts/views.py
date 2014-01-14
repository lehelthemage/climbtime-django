# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
import bson

from concepts.models import Concept, Feature, Property, PROPERTY_TYPE


def get_new_properties(request):

    new_properties = []

   #iterate once through the POST items to create the Property objects
    for i, v in request.POST.items():
        if i[:5] == "prop_" and len(i[5:]) < 3:
            if v == '' or request.POST["propval_" + i[5:]] == '':
                continue
            p = Property()
            f = Feature()
            p.feature = f
            p.property_id = i[5:]
            p.feature.title = v
            new_properties.append(p)

    #now iterate through POST list for property_type and value
    for i, v in request.POST.items():
        if i[:9] == "proptype_" and len(i[9:]) < 3:
            for new_property in new_properties:
                if new_property.property_id == i[9:]:
                    new_property.feature.property_type = v
                    break

        elif i[:8] == "propval_" and len(i[8:]) < 3:
            for new_property in new_properties:
                if new_property.property_id == i[8:]:
                    new_property.value = v
                    break

    return new_properties


def index(request):
    latest_concept_list = Concept.objects#.order_by('-pub_date')[:5]
    context = {
        'latest_concept_list': latest_concept_list
    }
    return render(request, 'concepts/index.html', context)


def conceptdetail(request, concept_id):
    try:
        concept = Concept.objects.get(id=concept_id)
    except Concept.DoesNotExist:
        raise Http404

    return render(request, 'concepts/conceptdetail.html',
                  {
                      'concept': concept,
                      'PROPERTY_TYPE': PROPERTY_TYPE})



def conceptupdate(request, concept_id):

    c = Concept.objects.get(id=concept_id)
    c.description = request.POST['description']

    property_deletions = []
    #update the properties
    for p in c.properties:
        p.feature.title = request.POST.get('prop_' + str(p.property_id), False)
        if not p.feature.title:
            property_deletions.append(p)
            continue
        p.feature.property_type = request.POST['proptype_' + str(p.property_id)]
        p.value = request.POST['propval_' + str(p.property_id)]
        f = p.feature
        f.save()


    #remove property_deletions
    for pd in property_deletions:
        for i, p in enumerate(c.properties):
            if p.property_id == pd.property_id:
                c.properties.pop(i)
                break

    #add new properties
    properties = get_new_properties(request)
    for p in properties:
        p.property_id = bson.ObjectId()
        c.properties.append(p)
        #ugly upsert (in case its not in db)
        Feature.objects(
            title=p.feature.title,
            is_property=p.feature.is_property,
            property_type=p.feature.property_type
            ).update_one(
            set__title=p.feature.title,
            set__is_property=p.feature.is_property,
            set__property_type=p.feature.property_type,
            upsert=True
        )

        f = Feature.objects.get(
            title=p.feature.title,
            is_property=p.feature.is_property,
            property_type=p.feature.property_type
            )

        p.feature = f


    c.save()

    return HttpResponseRedirect(reverse('concepts:conceptdetail', args=(c.id,)))

    def newconcept(request):
        return HttpResponse("under development.")

