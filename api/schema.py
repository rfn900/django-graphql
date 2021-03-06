import graphene
from stock.models import Stock
from portfolio.models import Portfolio, Trade
from stock.schema import StockType
from portfolio.schema import (
    PortfolioType,
    TradeType,
    CreatePortfolio,
    UpdatePortfolio,
)
from django.db.models import Sum
from graphql import GraphQLError


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

class SellStock(graphene.Mutation):
    trade = graphene.Field(TradeType)

    class Arguments:
        portfolio_id = graphene.Int()
        stock_symbol = graphene.String()
        price = graphene.Int()
        volume = graphene.Int()

    def mutate(self,info, portfolio_id, stock_symbol, price, volume):
        portfolio = Portfolio.objects.get(id=portfolio_id)

        trades = portfolio.trades.filter(stock_symbol=stock_symbol)
        sold = trades.filter(trade_type='S').aggregate(Sum('volume'))
        bought = trades.filter(trade_type='B').aggregate(Sum('volume'))

        if bought['volume__sum'] is None:
            raise GraphQLError('You do not own any volume of this stock')

        if sold['volume__sum'] is None:
            sold['volume__sum'] = 0

        available_volume = bought['volume__sum'] - sold['volume__sum']

        if available_volume < volume:
            raise GraphQLError("Not enough volume for this transaction!")

        new_trade = Trade(price=price, volume=volume,
                  trade_type='S',portfolio=portfolio,stock_symbol=stock_symbol)

        new_trade.save()
        portfolio.trades.add(new_trade)
        portfolio.account_balance = portfolio.account_balance + price*volume

        portfolio.save()
        return SellStock(trade=new_trade)


class BuyStock(graphene.Mutation):
    trade = graphene.Field(TradeType)

    class Arguments:
        portfolio_id = graphene.Int()
        stock_symbol = graphene.String()
        price = graphene.Int()
        volume = graphene.Int()

    def mutate(self,info, portfolio_id, stock_symbol, price, volume):
        portfolio = Portfolio.objects.get(id=portfolio_id)
        stock = Stock.objects.filter(symbol=stock_symbol)
        if not stock:
            raise GraphQLError('No stock found with this symbol')

        if price*volume > portfolio.account_balance:
            raise GraphQLError('You do not have sufficient funds for this')

        new_trade = Trade(price=price, volume=volume,
                  trade_type='B',portfolio=portfolio,stock_symbol=stock_symbol)

        new_trade.save()
        portfolio.trades.add(new_trade)
        portfolio.account_balance = portfolio.account_balance - price*volume

        portfolio.save()
        return BuyStock(trade=new_trade)


class Mutation(graphene.ObjectType):
    create_portfolio = CreatePortfolio.Field()
    update_portfolio = UpdatePortfolio.Field()
    sell_stock = SellStock.Field()
    buy_stock = BuyStock.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
