# SteamMarketTradingBot
 
## Project Overview
This project analyzes the price movements of items in the Steam Marketplace, particularly items associated with Dota 2 heroes. The goal is to identify systematic trading strategies by leveraging a hero's win rate, which impacts the demand for associated in-game items. The analysis combines historical data, machine learning models, and backtesting to test a trading strategy based on hero popularity and item price trends.

## Data Collection
1. Main Item List
The item list is built using the function build_item_list, which scrapes item data from the Steam Marketplace. This generates a subset of items, stored as CSV files for further analysis.
2. Price History
The process_price_history_row function collects price history data for items using the internal Steam Web API. Items with incomplete or missing price histories are filtered out to create a clean dataset for analysis.
3. Hero Data
Hero statistics such as win rates are obtained via the STRATZ API. Due to API limitations, only a single item is analyzed in detail, with future expansions planned to handle more items. For this project, the hero Lifestealer and his item, "Golden Dread Requisition," is the focus.

## Analysis Workflow
1. Data Manipulation
Datasets for both item prices and hero win rates are merged and resampled monthly. Lag features are generated for hero win rates and item prices to serve as inputs to predictive models.
2. Exploratory Data Analysis (EDA)
Visualizations are created to show the correlation between hero win rates and item prices. A 3-month simple moving average (SMA) is used to smooth win rate data and observe long-term trends.

## Predictive Modeling
1. Linear Regression
A linear regression model is used to predict item prices based on the current and lagged values of the hero's win percentage. While the R-squared value is low (0.139), the results show that win rate has some explanatory power.
2. Gradient Boosting (XGBoost)
An XGBoost regression model is applied to capture the relationship between hero win rates and item prices. The model uses multiple lagged values of win rates and prices to improve predictive power.

## Backtesting Strategy
1. Trading Strategy
The trading strategy buys an item when its predicted price exceeds the current price by 1% and sells when the predicted price falls below the current price by 1%. This is implemented using the Backtest library.
2. Results
The backtest results show that the strategy performs better than a buy-and-hold approach, with a 5.65% return compared to a -37% return for buy-and-hold. However, this is based on in-sample data, and further out-of-sample testing is required to confirm robustness.

## Future Work
Larger Dataset: Collecting more extensive historical data on hero win rates and popularity would allow for more comprehensive testing.
Additional Features: Incorporating other features such as Dota 2 tournament schedules, seasonality of player activity, and Steam sales events may improve the predictive accuracy of the models.