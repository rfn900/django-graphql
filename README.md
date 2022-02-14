# Django + GraphQL API

This Django project exposes a GraphQL API for querying stocks, portolios and
trades.

## How to run it

Make sure you have [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/install/)
installed locally.

- Clone this repository
- Run `docker-compose up` from the repo's root directory
- Once the _build_ is done, go to `http://localhost:8000/graphql/` and run the
  queries described bellow

## Todos

- [x] Querying all stocks
- [x] Query a single stock by symbol
- [x] Querying all portfolios
- [x] Query a single portfolio by id
- [x] Creating a portfolio with fields name, description and initial account balance
- [x] Editing a portfolio with fields name, description
- [x] Selling a stock, with fields for portfolio, stock, volume and price
- [x] Buying a stock, with fields for portfolio, stock, volume and price
- [x] Should only be able to buy a stock if one has enough funds
- [x] Should only be able to sell a stock if one is currently holding enough
      volume of the given stock

### Queries

#### 1 - Query all stocks

```graphql
{
  stocks {
    name
    symbol
  }
}
```

#### 2 - Query Stocks via symbol

```graphql
{
  stocksBySymbol(symbol: "ACA") {
    id
    name
    symbol
  }
}
```

#### 3 - Query all portfolios

```graphql
{
  portfolios {
    id
    name
    description
    initialAccountBalance
    accountBalance
    trades {
      id
      stockSymbol
      tradeType
      price
      volume
    }
  }
}
```

#### 4 - Query portfolios by id

```graphql
{
  portfoliosById(id: 1) {
    name
    description
    initialAccountBalance
    accountBalance
    trades {
      id
      price
      tradeType
      volume
    }
  }
}
```

#### 5 - Create a portfolio

```graphql
mutation {
  createPortfolio(
    name: "Crypto Bro!"
    description: "Dodge FTW"
    initialAccountBalance: 1000000
  ) {
    portfolio {
      id
      name
      description
    }
  }
}
```

#### 6 - Update a portfolio

```graphql
mutation {
  updatePortfolio(
    id: 1
    name: "Only Tech Stuff"
    description: "I'ms gonna gets risch"
  ) {
    portfolio {
      id
      name
      description
      accountBalance
    }
  }
}
```

#### 7 - Selling a stock

```graphql
mutation {
  sellStock(portfolioId: 1, price: 250, volume: 5, stockSymbol: "ABBV") {
    trade {
      id
    }
  }
}
```

#### 8 - Buying a stock

```graphql
mutation {
  buyStock(portfolioId: 2, price: 150, volume: 2, stockSymbol: "ACA") {
    trade {
      id
    }
  }
}
```
