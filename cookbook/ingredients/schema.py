import graphene
from graphene_django.types import DjangoObjectType
from ingredients.models import Category, Ingredient
from django.db.models import Q
from django.contrib.gis.geoip2 import GeoIP2

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient


class Query(object):
    all_categories = graphene.List(CategoryType)
    all_ingredients = graphene.List(IngredientType,
    							search=graphene.String(),
						        first=graphene.Int(),
						        skip=graphene.Int(),
    							)
    goodbye = graphene.String()

    your_location = graphene.String(required=True,ip=graphene.String())
    # your_location = graphene.JSONString(required=True,ip=graphene.String())

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_ingredients(self, info, search=None, first=None, skip=None,**kwargs):
        # We can easily optimize query count in the resolve method
        ing = Ingredient.objects.select_related('category').all()
        if search:
        	filter = (
        		Q(name__icontains=search)|
        		Q(notes__contains=search)
        		)
        	ing = ing.filter(filter)

        if skip:
        	ing = ing[skip:]
        if first:
        	ing = ing[:first]

       	return ing

    def resolve_goodbye(self, info):
    	return 'See ya!'

    def resolve_your_location(self,info,**kwargs):
        geo_location_obj = GeoIP2()
        # my_ip = info.context.META.get('REMOTE_ADDR')
        my_ip='43.254.162.207'
        x_forwarded_for = info.context.META.get('HTTP_X_FORWARDED_FOR',my_ip)
        hostname = kwargs.get('ip',my_ip) 
        city_json_val = geo_location_obj.city(hostname)
        return city_json_val