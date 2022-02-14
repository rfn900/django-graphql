# Django + GraphQL API

This Django project exposes a GraphQL API for querying stocks, portolios and
trades.

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
