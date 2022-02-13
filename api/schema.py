import graphene
from graphene_django import DjangoObjectType
from .models import Stock, Portfolio, Trade
from django.db.models import Sum
from graphql import GraphQLError

class StockType(DjangoObjectType):
    class Meta:
        model = Stock
        fields = (
            'id',
            'name',
            'symbol',
        )

class PortfolioType(DjangoObjectType):
    class Meta:
        model = Portfolio
        fields = (
            'id',
            'name',
            'description',
            'initial_account_balance',
            'account_balance',
            'trades'
        )

    @graphene.resolve_only_args
    def resolve_trades(self):
        return self.trades.all()

class TradeType(DjangoObjectType):
    class Meta:
        model = Trade
        fields = (
            'id',
            'price',
            'volume',
            'trade_type',
            'portfolio',
            'stock_symbol',
        )


class CreatePortfolio(graphene.Mutation):
    portfolio = graphene.Field(PortfolioType)

    class Arguments:
        name = graphene.String()
        description = graphene.String()
        initial_account_balance = graphene.Int()
        account_balance = graphene.Int()

    def mutate(self, info, name, description, initial_account_balance):
        new_portfolio = Portfolio(name=name, description=description,
                                    initial_account_balance=initial_account_balance,
                                  account_balance=initial_account_balance)
                                  
        new_portfolio.save()
        return CreatePortfolio(portfolio=new_portfolio)


class Query(graphene.ObjectType):
    stocks = graphene.List(StockType)
    portfolios = graphene.List(PortfolioType)
    trades = graphene.List(TradeType)
    stocks_by_symbol = graphene.List(StockType, symbol=graphene.String())
    portfolios_by_id = graphene.Field(PortfolioType, id=graphene.Int())
    def resolve_stocks(self,info):
        return Stock.objects.all()
    def resolve_portfolios(self,info):
        return Portfolio.objects.all()
    def resolve_trades(self,info):
        return Trade.objects.all()

    def resolve_stocks_by_symbol(self, info, symbol):
        return Stock.objects.filter(symbol=symbol)

    def resolve_portfolios_by_id(self, indo, id):
        return Portfolio.objects.get(pk=id)

class Mutation(graphene.ObjectType):
    create_portfolio = CreatePortfolio.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)
