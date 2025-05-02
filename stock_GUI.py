from datetime import datetime
import tkinter as tk
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import csv
import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData
class StockApp:
    def __init__(self):
        if not os.path.exists("stocks.db"):
            stock_data.create_database()
        self.stock_list = []
        self.root = tk.Tk()
        self.root.title("Stock Manager")
        # Menubar Setup
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Data", command=self.load)
        file_menu.add_command(label="Save Data", command=self.save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        # Chart Menu
        chart_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Chart", menu=chart_menu)
        chart_menu.add_command(label="Show Chart", command=self.display_chart)
        data_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Data", menu=data_menu)
        data_menu.add_command(label="Import from Web", command=self.scrape_web_data)
        data_menu.add_command(label="Import from CSV", command=self.importCSV_web_data)
        # Tabs Setup
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True)
        self.main_tab = tk.Frame(notebook)
        self.history_tab = tk.Frame(notebook)
        self.report_tab = tk.Frame(notebook)
        notebook.add(self.main_tab, text='Main')
        notebook.add(self.history_tab, text='History')
        notebook.add(self.report_tab, text='Report')
        self.headingLabel = tk.Label(self.main_tab, text="Select a stock to view details", font=('Arial', 12, 'bold'))
        self.headingLabel.pack(pady=5)
        # Stock Listbox
        self.stock_listbox = tk.Listbox(self.main_tab)
        self.stock_listbox.pack(fill='both', expand=True)
        self.stock_listbox.bind('<<ListboxSelect>>', self.display_stock_data)
        # Entry widgets for adding a stock
        self.addSymbolEntry = tk.Entry(self.main_tab)
        self.addSymbolEntry.pack()
        self.addSymbolEntry.insert(0, "Symbol")
        self.addNameEntry = tk.Entry(self.main_tab)
        self.addNameEntry.pack()
        self.addNameEntry.insert(0, "Name")
        self.addSharesEntry = tk.Entry(self.main_tab)
        self.addSharesEntry.pack()
        self.addSharesEntry.insert(0, "Shares")
        add_button = tk.Button(self.main_tab, text="Add Stock", command=self.add_stock)
        add_button.pack()
        # Entry for buying/selling shares
        self.updateSharesEntry = tk.Entry(self.main_tab)
        self.updateSharesEntry.pack()
        self.updateSharesEntry.insert(0, "Shares to Buy/Sell")
        buy_button = tk.Button(self.main_tab, text="Buy Shares", command=self.buy_shares)
        buy_button.pack()
        sell_button = tk.Button(self.main_tab, text="Sell Shares", command=self.sell_shares)
        sell_button.pack()
        delete_button = tk.Button(self.main_tab, text="Delete Stock", command=self.delete_stock)
        delete_button.pack()
        # History and Report Text Widgets
        self.history_text = tk.Text(self.history_tab)
        self.history_text.pack(fill='both', expand=True)
        self.report_text = tk.Text(self.report_tab)
        self.report_text.pack(fill='both', expand=True)   
        # Load data on start
        self.load()
    # Load stocks and history from database.
    def load(self):
        self.stock_list.clear()
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)
        self.stock_listbox.delete(0, tk.END)
        for stock in self.stock_list:
            self.stock_listbox.insert(tk.END, stock.symbol)
        messagebox.showinfo("Load Data", "Data Loaded")
    # Save stocks and history to database.
    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data", "Data Saved")
        if self.stock_listbox.curselection():
            self.display_stock_data()
    # Display stock price and volume history.
    def display_stock_data(self, event=None):
        selected_symbol = self.stock_listbox.get(self.stock_listbox.curselection())
        stock = next((s for s in self.stock_list if s.symbol == selected_symbol), None)
        if stock:
            # Clear the text widgets before displaying new data
            self.history_text.delete(1.0, tk.END)
            self.report_text.delete(1.0, tk.END) 
            # Display stock history data
            for data in stock.DataList:
                self.history_text.insert(tk.END, f"{data.date.strftime('%m/%d/%Y')} - {data.close} - {data.volume}\n")       
            # Display stock report
            self.report_text.insert(tk.END, f"Stock: {stock.name} ({stock.symbol})\n")
            self.report_text.insert(tk.END, f"Shares: {stock.shares}\n")
            self.report_text.insert(tk.END, f"Total Value: ${stock.shares * stock.DataList[-1].close if stock.DataList else 0:,.2f}\n")
    # Add new stock to track.
    def add_stock(self):
        new_stock = Stock(self.addSymbolEntry.get(), self.addNameEntry.get(), float(self.addSharesEntry.get()))
        self.stock_list.append(new_stock)
        self.stock_listbox.insert(tk.END, self.addSymbolEntry.get())
        self.addSymbolEntry.delete(0, tk.END)
        self.addNameEntry.delete(0, tk.END)
        self.addSharesEntry.delete(0, tk.END)
    # Buy shares of stock.
    def buy_shares(self):
        selection = self.stock_listbox.curselection()
        if not selection:
            messagebox.showerror("No Selection", "Please select a stock first.")
            return
        symbol = self.stock_listbox.get(selection)
        #symbol = self.stock_listbox.get(self.stock_listbox.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.buy(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = f"{stock.name} - {stock.shares} Shares"
        messagebox.showinfo("Buy Shares", "Shares Purchased")
        self.updateSharesEntry.delete(0, tk.END)
    # Sell shares of stock.
    def sell_shares(self):
        selection = self.stock_listbox.curselection()
        if not selection:
            messagebox.showerror("No Selection", "Please select a stock first.")
            return
        symbol = self.stock_listbox.get(selection)
        # symbol = self.stock_listbox.get(self.stock_listbox.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.sell(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = f"{stock.name} - {stock.shares} Shares"
        messagebox.showinfo("Sell Shares", "Shares Sold")
        self.updateSharesEntry.delete(0, tk.END)
    # Remove stock and all history from being tracked.
    def delete_stock(self):
        selection = self.stock_listbox.curselection()
        if not selection:
            messagebox.showerror("No Selection", "Please select a stock first.")
            return
        symbol = self.stock_listbox.get(selection)
        # symbol = self.stock_listbox.get(self.stock_listbox.curselection())
        stock = next((s for s in self.stock_list if s.symbol == symbol), None)
        if stock:
            self.stock_list.remove(stock)
            self.stock_listbox.delete(self.stock_listbox.curselection())
            import sqlite3
            conn = sqlite3.connect("stocks.db")
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM dailyData WHERE symbol = ?", (symbol,))
                cur.execute("DELETE FROM stocks WHERE symbol = ?", (symbol,))
                conn.commit()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error deleting stock from database: {e}")
            finally:
                conn.close()
            messagebox.showinfo("Delete Stock", f"Stock {symbol} deleted.")
        else:
            messagebox.showerror("Delete Error", "Stock not found!")
    # Get data from web scraping.
    def scrape_web_data(self):
        symbol = simpledialog.askstring("Stock Symbol", "Enter Stock Symbol")
        if not symbol:
            messagebox.showerror("Missing Symbol", "You must enter a stock symbol.")
            return
        symbol = symbol.upper()
        dateFrom = simpledialog.askstring("Starting Date", "Enter Starting Date (m/d/yy)")
        dateTo = simpledialog.askstring("Ending Date", "Enter Ending Date (m/d/yy)")
        stock = next((s for s in self.stock_list if s.symbol == symbol), None)
        if not stock:
            # Create a new Stock instance with default values
            name = symbol  # Default to symbol as name
            stock = Stock(symbol, name, 0.0)
            self.stock_list.append(stock)
            self.stock_listbox.insert(tk.END, symbol)
        try:
            stock_data.retrieve_stock_web(dateFrom, dateTo, [stock])  # unchanged call
        except Exception as e:
            messagebox.showerror("Web Scraping Failed", f"Error: {e}")
            return
        self.display_stock_data()
        messagebox.showinfo("Data Retrieved", f"Web data for {symbol} has been added.")
    # Import CSV stock history file.
    def importCSV_web_data(self):
        symbol = self.stock_listbox.get(self.stock_listbox.curselection())
        filename = filedialog.askopenfilename(title=f"Select {symbol} File to Import", filetypes=[('Yahoo Finance! CSV', '*.csv')])
        filename = filename.strip('"').replace('\\', '/')
        if filename:
            stock_data.import_stock_web_csv(self.stock_list, symbol, filename)
            self.display_stock_data()
            messagebox.showinfo("Import Complete", f"{symbol} Import Complete")
    # Display stock price chart.
    def display_chart(self):
        selected_symbol = self.stock_listbox.get(self.stock_listbox.curselection())
        stock = next((s for s in self.stock_list if s.symbol == selected_symbol), None)
        if stock and stock.DataList:
            display_stock_chart(self.stock_list, selected_symbol)
        else:
            messagebox.showwarning("No Data", "No data available to display chart.")
# Main function to run the app
def main():
    app = StockApp()
    app.root.mainloop()
if __name__ == "__main__":
    main()