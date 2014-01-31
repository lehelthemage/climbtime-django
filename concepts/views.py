# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.decorators import login_required
from mongoengine import DoesNotExist
from mongoengine.django.auth import User
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
import bson
import simplejson

from concepts.models import Concept, Feature, Property, Category, PROPERTY_TYPE


def get_new_properties(request, for_category):
    new_properties = []

    #iterate once through the POST items to create the Property objects
    for i, v in request.POST.items():

        if i[:5] == "prop_" and len(i[5:]) < 3:

            if v == '' or (not for_category and request.POST.get("propval_" + i[5:], False) is False):
                continue

            f = Feature()

            if for_category:
                f.id = i[5:]
                f.title = v
                new_properties.append(f)
            else:
                p = Property()
                p.feature = f
                p.property_id = i[5:]
                p.feature.title = v
                new_properties.append(p)



    #now iterate through POST list for property_type and value
    for i, v in request.POST.items():
        if i[:9] == "proptype_" and len(i[9:]) < 3:
            for new_property in new_properties:
                if for_category:
                    if new_property.id == i[9:]:
                        new_property.property_type = v
                else:
                    if new_property.property_id == i[9:]:
                        new_property.feature.property_type = v
                break

        elif i[:8] == "propval_" and len(i[8:]) < 3:
            for new_property in new_properties:
                if new_property.property_id == i[8:]:
                    new_property.value = v
                    break

    return new_properties

@login_required
def index(request):
    latest_concept_list = Concept.objects#.order_by('-pub_date')[:5]
    context = {
        'latest_concept_list': latest_concept_list
    }
    return render(request, 'concepts/index.html', context)


def concept_detail(request, concept_id):
    try:
        concept = Concept.objects.get(id=concept_id)
    except Concept.DoesNotExist:
        raise Http404

    return render(request, 'concepts/conceptdetail.html',
                  {
                      'concept': concept,
                      'PROPERTY_TYPE': PROPERTY_TYPE})


def update_properties(request, c, for_category):
    if not for_category:
        properties = c.properties
    else:
        properties = c.features

    property_deletions = []
    #update the properties
    for property in properties:
        if for_category:
            property_id = property.id
        else:
            property_id = property.property_id

        title = request.POST.get('prop_' + str(property_id), False)
        if not title:
            property_deletions.append(property)
            continue

        property_type = request.POST['proptype_' + str(property_id)]

        if not for_category:
            property_value = request.POST['propval_' + str(property_id)]

        if for_category:
            f = property
        else:
            f = property.feature

        f.title = title
        f.property_type = property_type
        f.save()

    #remove property_deletions
    for pd in property_deletions:
        for i, p in enumerate(properties):
            if for_category:
                if p.id == pd.id:
                    properties.pop(i)
            elif p.property_id == pd.property_id:
                properties.pop(i)
                break

    #add new properties
    new_properties = get_new_properties(request, for_category)
    for i, new_property in enumerate(new_properties):
        if not for_category:
            new_property.property_id = bson.ObjectId()

        #ugly upsert (in case its not in db)
        if for_category:
            title = new_property.title
            is_property = new_property.is_property
            property_type = new_property.property_type
        else:
            title = new_property.feature.title
            is_property = new_property.feature.is_property
            property_type = new_property.feature.property_type

        Feature.objects(
            title=title,
            is_property=is_property,
            property_type=property_type
        ).update_one(
            set__title=title,
            set__is_property=is_property,
            set__property_type=property_type,
            upsert=True
        )

        f = Feature.objects.filter(
            title=title,
            is_property=is_property,
            property_type=property_type
        )[0]

        if for_category:
            c.features.append(f)
        else:
            new_property.feature = f
            c.properties.append(new_property)


def concept_update(request, concept_id):
    c = Concept.objects.get(id=concept_id)
    c.description = request.POST['description']
    update_properties(request, c, False)
    c.save()

    return HttpResponseRedirect(reverse('concepts:conceptdetail', args=(c.id,)))


def new_concept(request):
    return render(request, 'concepts/newcconcept.html')


def add_concept(request):
    new_con = Concept()

    new_con.title = request.POST['title']
    new_con.description = request.POST['description']
    new_con.parent = None

    form_properties = get_new_properties(request, True)

    for form_property in form_properties:
        #ugly upsert (in case its not in db)
        Feature.objects(
            title=form_property.title,
            is_property=True,
            property_type=form_property.property_type
        ).update_one(
            set__title=form_property.title,
            set__is_property=True,
            set__property_type=form_property.property_type,
            upsert=True)

        new_feature = Feature.objects.filter(
            title=form_property.title,
            is_property=True,
            property_type=form_property.property_type
        )[0]

        new_property = Property(
            feature=new_feature,
            property_id=bson.ObjectId(),
            value=form_property.value)
        new_con.properties.append(new_property)

    new_con.save()

    return HttpResponseRedirect(reverse('concepts:conceptdetail', args=(new_con.id,)))

@login_required
def new_category(request):
    return render(request, 'concepts/newcategory.html', {'user': request.user})


def add_category(request):
    new_cat = Category()

    new_cat.title = request.POST['title']
    new_cat.description = request.POST['description']
    new_cat.parent = None

    form_properties = get_new_properties(request, True)

    for form_property in form_properties:
        #ugly upsert (in case its not in db)
        Feature.objects(
            title=form_property.title,
            is_property=True,
            property_type=form_property.property_type
        ).update_one(
            set__title=form_property.title,
            set__is_property=True,
            set__property_type=form_property.property_type,
            upsert=True)

        feature = Feature.objects.filter(
            title=form_property.title,
            is_property=True,
            property_type=form_property.property_type
        )[0]

        new_cat.features.append(feature)

    new_cat.save()

    return HttpResponseRedirect(reverse('concepts:categorydetail', args=(new_cat.id,)))


def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    return render(request, 'concepts/categorydetail.html',
                  {
                      'category': category,
                      'PROPERTY_TYPE': PROPERTY_TYPE})


def category_update(request, category_id):
    c = Category.objects.get(id=category_id)
    c.description = request.POST['description']
    c.parent = Category.objects.get(id=request.POST['parent_id'])
    update_properties(request, c, True)
    c.save()

    return HttpResponseRedirect(reverse('concepts:categorydetail', args=(category_id,)))


def concept_ajax_features(request):
    return HttpResponse("under development.")


def autocomplete_parents(request):
    if request.is_ajax():
        callback = request.GET.get('callback', '')
        starts_with = request.GET.get('term', '')
        parents = Category.objects.filter(title__istartswith=starts_with)

        results = []
        for parent in parents:
            req = {}
            req['id'] = str(parent.id)
            req['title'] = parent.title
            results.append(req)

        response = simplejson.dumps(results)
        response = callback + '(' + response + ');'
    else:
        response = 'fail'

    return HttpResponse(response, mimetype="application/json")


def get_category_properties(request):

    callback = request.GET.get('callback', '')
    category_id = request.GET.get('category_id', '')

    if request.is_ajax():
        category = Category.objects.get(id=category_id)

        results = []
        for category_features in category.parent.features:
            if not category_features.is_property:
                continue

            req = {}
            req['title'] = category_features.title
            req['property_type'] = category_features.property_type
            results.append(req)

        response = simplejson.dumps(results)
        response = callback + '(' + response + ');'

    else:
        response = 'fail'

    return HttpResponse(response, mimetype="application/json")


def login_view(request):
    return render(request, 'concepts/login.html')

def login(request):
    try:
        uname = request.POST['username']
        passwd = request.POST['password']
        user = User.objects.get(username=uname)
        if user.check_password(passwd):
            user.backend = 'mongoengine.django.auth.MongoEngineBackend'
            user = authenticate(username=uname, password=passwd)
            auth_login(request, user)
            request.session.set_expiry(60 * 60 * 1) # 1 hour timeout
            return HttpResponseRedirect(reverse('concepts:newcategory'))
        else:
            return HttpResponse('login failed')
    except DoesNotExist:
        return HttpResponse('user does not exist')
    except Exception, e:
        return HttpResponse(e.message)


def logout_view(request):
    logout(request)
    return render(request, 'concepts/login.html')

