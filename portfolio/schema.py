import graphene
from graphene_django import DjangoObjectType
from .models import Portfolio, Trade


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


class UpdatePortfolio(graphene.Mutation):
    portfolio = graphene.Field(PortfolioType)

    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        description = graphene.String()
    
    def mutate(self, info, id, name, description):
        p = Portfolio.objects.get(id=id)
    
        p.name = name
        p.description = description
        p.save()
        
        return UpdatePortfolio(portfolio=p)
