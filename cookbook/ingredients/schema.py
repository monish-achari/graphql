import graphene
from graphene_django.types import DjangoObjectType
from ingredients.models import Category, Ingredient
from django.db.models import Q

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

