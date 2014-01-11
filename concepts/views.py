# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
import bson

from concepts.models import Concept, Feature, Property, PROPERTY_TYPE


def get_properties(request):
    for i, v in request.POST.items():
        if i[:5] == "prop_":





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
    for p in c.properties:
        p.feature.title = request.POST['prop_' + str(p.property_id)]
        p.feature.property_type = request.POST['proptype_' + str(p.property_id)]
        p.value = request.POST['propval_' + str(p.property_id)]
        if p.value == '':
            property_deletions.append(p)

    #remove property_deletions
    for pd in property_deletions:
        for i, p in enumerate(c.properties):
            if p.property_id == pd.property_id:
                c.properties.pop(i)
                break


    c.save()
    return HttpResponseRedirect(reverse('concepts:conceptdetail', args=(c.id,)))

    def newconcept(request):
        return HttpResponse("under development.")

