#Helper Functions
import matplotlib.pyplot as plt
from os import system, name
# Function to Clear the Screen
def clear_screen():
    if name == "nt": # User is running Windows
        _ = system('cls')
    else: # User is running Linux or Mac
        _ = system('clear')
# Function to sort the stock list (alphabetical)
def sortStocks(stock_list):
    # Sort the stock list
    stock_list.sort(key = lambda stock: stock.symbol.upper())
# Function to sort the daily stock data (oldest to newest) for all stocks
def sortDailyData(stock_list):
    for stock in stock_list:
        stock.DataList.sort(key = lambda data: data.date)
# Function to create stock chart
def display_stock_chart(stock_list, symbol):
    for stock in stock_list:
        if stock.symbol == symbol:
            dates = [data.date for data in stock.DataList]
            prices = [data.close for data in stock.DataList]
            volumes = [data.volume for data in stock.DataList]
            if not dates:
                print("No data available to display chart.")
                return
            fig, ax1 = plt.subplots(figsize = (10, 5))
            ax1.set_title(f"{stock.name} ({stock.symbol}) - Price and Volume Chart")
            ax1.set_xlabel("Date")
            ax1.set_ylabel("Price ($)", color = "tab:blue")
            ax1.plot(dates, prices, color = "tab:blue", label = "Price")
            ax1.tick_params(axis = "y", labelcolor = "tab:blue")
            ax2 = ax1.twinx()
            ax2.set_ylabel("Volume", color = "tab:red")
            ax2.bar(dates, volumes, color = "tab:red", alpha = 0.3, label = "Volume")
            ax2.tick_params(axis = "y", labelcolor = "tab:red")
            fig.tight_layout()
            plt.show()
            return
    print(f"Stock symbol '{symbol}' not found.")