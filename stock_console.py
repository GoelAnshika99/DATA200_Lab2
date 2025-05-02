# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.
from datetime import datetime
from stock_class import Stock, DailyData
import sqlite3
from utilities import clear_screen, display_stock_chart
from os import path
import stock_data
# Main Menu
def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","5","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        else:
            clear_screen()
            print("Goodbye")
# Manage Stocks
def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ")
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")
# Add new stock to track
def add_stock(stock_list):
    symbol = input("Enter Stock Symbol: ").upper()
    name = input("Enter Stock Name: ")
    shares = float(input("Enter Number of Shares: "))
    stock = Stock(symbol, name, shares)
    stock_list.append(stock)
    print(f"Stock {symbol} added successfully!")
    input("Press Enter to continue......")
# Buy or Sell Shares Menu
def update_shares(stock_list):
    symbol = input("Enter Stock Symbol to update: ").upper()
    stock = next((s for s in stock_list if s.symbol == symbol), None)
    if stock:
        option = input("1 - Buy Shares\n2 - Sell Shares\nEnter Option: ")
        if option == "1":
            buy_stock(stock)
        elif option == "2":
            sell_stock(stock)
    else:
        print("Stock not found!")
    input("Press Enter to continue....")
# Buy Stocks (add to shares)
def buy_stock(stock):
    shares = float(input("Enter the number of shares to buy: "))
    stock.buy(shares)
    print(f"{shares} shares added to {stock.symbol}. Total shares: {stock.shares}")
# Sell Stocks (subtract from shares)
def sell_stock(stock):
    shares = float(input("Enter number of shares to sell: "))
    if shares > stock.shares:
        print("Not enough shares to sell!")
    else:
        stock.sell(shares)
        print(f"{shares} shares sold from {stock.symbol}. Total shares: {stock.shares}")
# Remove stock and all daily data
def delete_stock(stock_list):
    symbol = input("Enter Stock Symbol to delete: ").upper()
    stock = next((s for s in stock_list if s.symbol == symbol), None)
    if stock:
        stock_list.remove(stock)
        print(f"Stock {symbol} and its data deleted from list.")
        try:
            conn = sqlite3.connect("stocks.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM stocks WHERE symbol = ?", (symbol,))
            cursor.execute("DELETE FROM dailyData WHERE symbol = ?", (symbol,))
            conn.commit()
            conn.close()
            print(f"Stock {symbol} and its data deleted from the database.")
        except sqlite3.Error as e:
            print(f"Error deleting stock from database: {e}")
    else:
        print("Stock not found!")
    input("Press Enter to continue.....")
# List stocks being tracked
def list_stocks(stock_list):
    clear_screen()
    if not stock_list:
        print("No stocks are being tracked.")
    else:
        print("Tracked Stocks:")
        for stock in stock_list:
            print(f"Symbol: {stock.symbol}, Name: {stock.name}, Shares: {stock.shares}")
    input("Press Enter to continue....")
# Add Daily Stock Data
def add_stock_data(stock_list):
    symbol = input("Enter Stock Symbol to add data to: ").upper()
    stock = next((s for s in stock_list if s.symbol == symbol), None)
    if stock:
        date_str = input("Enter Date (MM/DD/YYYY): ")
        date = datetime.strptime(date_str, "%m/%d/%Y")
        price = float(input("Enter Price: "))
        volume = float(input("Enter Volume: "))
        daily_data = DailyData(date, price, volume)
        stock.add_data(daily_data)
        print(f"Data for {symbol} on {date_str} added successfully!")
    else:
        print("Stock not found!")
    input("Press Enter to continue.....")
# Display Report for All Stocks
def display_report(stock_list):
    clear_screen()
    print("Stock Report ---")
    if not stock_list:
        print("No stocks to report.")
    else:
        for stock in stock_list:
            print(f"\nStock: {stock.symbol}, {stock.name}")
            for data in stock.DataList:
                print(f"Date: {data.date.strftime('%m/%d/%Y')}, Price: {data.close}, Volume: {data.volume}")
    input("Press Enter to continue.....")
# Display Chart
def display_chart(stock_list):
    clear_screen()
    symbol = input("Enter Stock Symbol to display chart: ").upper()
    stock = next((s for s in stock_list if s.symbol == symbol), None)
    if stock:
        display_stock_chart(stock_list, symbol)
    else:
        print("Stock not found!")
    input("Press Enter to continue....")
# Manage Data Menu
def manage_data(stock_list):
    option = ""
    while option != "0":
        # clear_screen()
        print("Manage Data ---")
        print("1 - Save Data to Database")
        print("2 - Load Data from Database")
        print("3 - Retrieve Stock Data from Web")
        print("4 - Import Data from CSV")
        print("0 - Exit Manage Data")
        option = input("Enter Menu Option: ")
        while option not in ["1", "2", "3", "4", "0"]:
            # clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Manage Data ---")
            print("1 - Save Data to Database")
            print("2 - Load Data from Database")
            print("3 - Retrieve Stock Data from Web")
            print("4 - Import Data from CSV")
            print("0 - Exit Manage Data")
            option = input("Enter Menu Option: ")
        if option == "1":
            stock_data.save_stock_data(stock_list)
            print("Data saved to database.")
        elif option == "2":
            stock_data.load_stock_data(stock_list)
            if stock_list:
                print("\nStocks loaded from database:")
                for stock in stock_list:
                    print(f"{stock.symbol} - {stock.name} - {stock.shares} shares")
                    for data in stock.DataList:
                        print(f"  {data.date.strftime('%m/%d/%Y')} - ${data.close:.2f} - Volume: {data.volume}")
            else:
                print("No data found in the database.")
            print("Data loaded from database.")
        elif option == "3":
            date_start = input("Enter start date (MM/DD/YYYY): ")
            date_end = input("Enter end date (MM/DD/YYYY): ")
            record_count = stock_data.retrieve_stock_web(date_start, date_end, stock_list)
            print(f"{record_count} records retreived from the web.")
        elif option == "4":
            symbol = input("Enter Stock Symbol to import CSV for: ").upper()
            filename = input("Enter CSV filename: ")
            filename = filename.strip('"').replace('\\', '/')
            stock_data.import_stock_web_csv(stock_list, symbol, filename)
            print(f"Data imported from {filename}.")
        else:
            print("Returning to Main Menu")
    input("Press Enter to continue.....")
# Get stock price and volume history from Yahoo! Finance using Web Scraping
# def retrieve_from_web(stock_list):
#     clear_screen()
#     pass
# # Import stock price and volume history from Yahoo! Finance using CSV Import
# def import_csv(stock_list):
#     clear_screen()
#     pass
# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)
# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()