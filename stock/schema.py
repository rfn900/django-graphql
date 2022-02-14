from graphene_django import DjangoObjectType
from .models import Stock

class StockType(DjangoObjectType):
    class Meta:
        model = Stock
        fields = (
            'id',
            'name',
            'symbol',
        )
