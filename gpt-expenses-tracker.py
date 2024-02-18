import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import requests

class MoneyTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Money Tracker💸")
        self.root.geometry("900x500")
        self.expenses_list = []
        self.setup_ui()

    def setup_ui(self):
        # Add all the UI components to the window
        self.create_widgets()
        self.create_treeview()
        self.layout_widgets()

   

    def create_widgets(self):
        """Create and layout the input widgets for expense data entry."""
        self.frame_entry = tk.Frame(self.root)
        
        # Amount
        self.label_amount = tk.Label(self.frame_entry, text="Amount Spent:")
        self.entry_amount = tk.Entry(self.frame_entry)
        
        # Currency
        self.label_currency = tk.Label(self.frame_entry, text="Amount Currency:")
        self.combo_currencies = ttk.Combobox(self.frame_entry, values=["EGP", "USD", "EUR", "GBP"])
        
        # Category
        self.label_category = tk.Label(self.frame_entry, text="Category:")
        self.combo_category = ttk.Combobox(self.frame_entry, values=["Daily Expenses", "Shopping", "Internet & phone", "Transportation", "Hanging out", "Savings", "Family", "Urgent", "Coffee"])
        
        # Payment Method
        self.label_method = tk.Label(self.frame_entry, text="Payment Method:")
        self.combo_method_payment = ttk.Combobox(self.frame_entry, values=["Cash", "Visa", "Vodafone Cash", "Online Card", "PayPal"])
        
        # Date
        self.label_date = tk.Label(self.frame_entry, text="Date:")
        self.entry_date = DateEntry(self.frame_entry, selectmode="day")
        
        # Add Button
        self.button_add = tk.Button(self.frame_entry, text="Add Expense", command=self.add_expenses)
        
        # Layout the widgets in the frame
        self.label_amount.grid(row=0, column=0, padx=5, pady=5)
        self.entry_amount.grid(row=0, column=1, padx=5, pady=5)
        self.label_currency.grid(row=0, column=2, padx=5, pady=5)
        self.combo_currencies.grid(row=0, column=3, padx=5, pady=5)
        self.label_category.grid(row=1, column=0, padx=5, pady=5)
        self.combo_category.grid(row=1, column=1, padx=5, pady=5)
        self.label_method.grid(row=1, column=2, padx=5, pady=5)
        self.combo_method_payment.grid(row=1, column=3, padx=5, pady=5)
        self.label_date.grid(row=2, column=0, padx=5, pady=5)
        self.entry_date.grid(row=2, column=1, padx=5, pady=5)
        self.button_add.grid(row=2, column=3, padx=5, pady=5)

    def create_treeview(self):
        """Create and layout the Treeview for displaying expenses."""
        self.treeview = ttk.Treeview(self.root, columns=('date', 'category', 'amount', 'currency', 'payment_method'), show='headings')
        
        # Define headings and column configurations
        for col in self.treeview['columns']:
            self.treeview.heading(col, text=col.capitalize())
            self.treeview.column(col, width=120, anchor="center")
        
        # Scrollbar for the Treeview
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scrollbar.set)

        # Style configuration for Treeview
        self.style = ttk.Style(self.root)
        self.style.configure("Treeview.Heading", font=('Calibri', 10, 'bold'), foreground="blue")
        self.style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 10))
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

    # ... (rest of the MoneyTracker class)


    def layout_widgets(self):
        # Layout all the widgets in the window
        self.frame_entry.grid(row=0, column=0, sticky="ew")
        # ...

        # Layout the treeview
        self.treeview.grid(row=7, column=0, columnspan=4, sticky='nsew')
        # ...

   
    def add_expenses(self):
        """Validate the user input and add the expense to the Treeview and internal list."""
        # Validate the amount; if it's not valid, a warning message will pop up and the function will return early
        amount = self.validate_numbers(self.entry_amount.get())
        if amount is None:
            return
        
        # Get the other values from the UI
        currency = self.combo_currencies.get()
        category = self.combo_category.get()
        date = self.get_date()  # Get the date from the DateEntry widget
        payment_method = self.combo_method_payment.get()
        
        # Check if all fields are filled
        if not (amount and currency and category and payment_method and date):
            messagebox.showwarning("Warning", "All fields are required.")
            return

        # Create the expense record
        expense_record = {
            "amount": amount,
            "currency": currency,
            "category": category,
            "date": date,
            "payment_method": payment_method
        }
        
        # Add the expense to the internal list and display it
        self.expenses_list.append(expense_record)
        self.display_expenses(expense_record)
        self.update_total_row()
        
        # Clear the input fields after adding
        self.entry_amount.delete(0, tk.END)
        self.combo_currencies.set('')
        self.combo_category.set('')
        self.combo_method_payment.set('')
        
    def validate_numbers(self, amount_str):
        """Validate that the amount is a number."""
        try:
            return float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the amount.")
            return None

    def get_date(self):
        """Retrieve the date from the DateEntry widget."""
        return self.entry_date.get_date().strftime("%Y-%m-%d")

    # ... (rest of the MoneyTracker class)


    def display_expenses(self, record):
        """Display a new record in the treeview."""
        self.treeview.insert('', 'end', values=(
                record['date'],
                record['category'],
                record['amount'],
                record['currency'],
                record['payment_method'],
        ))

    def convert_to_usd(self, amount, currency):
        """Converts an amount from a specified currency to USD."""
        if currency == "USD":
            return amount  # No conversion needed if it's already in USD
        
        # Check if the amount is a valid number
        try:
            amount = float(amount)
        except ValueError:
            raise ValueError(f"The amount '{amount}' is not a valid number.")
        
        # Check if the currency code is valid (3 letters)
        if not isinstance(currency, str) or len(currency) != 3:
            raise ValueError(f"The currency '{currency}' is not a valid currency code.")
        
        # Make an API request to get the conversion rates
        api_key = "24c9f38ded444584902523b5ed1a8da6"  
        request_url = f'https://api.currencyfreaks.com/v2.0/rates/latest?apikey={api_key}'
        try:
            response = requests.get(request_url)
            response.raise_for_status()  # Raise an error for bad status codes
            rates = response.json()['rates']
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to the currency conversion API: {e}")
        
        usd_rate = rates.get(currency)
        if usd_rate is None:
            raise LookupError(f"Could not find a conversion rate for {currency}.")
        
        converted_amount = round(amount / float(usd_rate), 2)
        return converted_amount    # Converts an amount from a specified currency to USD
        # ...

    def update_total_row(self):
        """Update the total row in the treeview with a yellow background."""
        # Remove any existing total row
        for item in self.treeview.get_children():
            if 'total' in self.treeview.item(item, 'tags'):
                self.treeview.delete(item)

        # Calculate the total expenditures in USD
        total_expenditures = 0
        for record in self.expenses_list:
            # Convert each amount to USD and sum them up
            try:
                amount_in_usd = self.convert_to_usd(record['amount'], record['currency'])
                if amount_in_usd is not None:
                    total_expenditures += amount_in_usd
            except (ValueError, LookupError, ConnectionError) as e:
                messagebox.showerror("Error", str(e))
                return

        # Insert the new total row at the end of the Treeview with a yellow background
        self.treeview.tag_configure('total', background='yellow')
        self.treeview.insert('', 'end', values=("Total", "",  total_expenditures,"USD", ""), tags=('total',))



# Main application logic
if __name__ == '__main__':
    window = tk.Tk()
    app = MoneyTracker(window)
    window.mainloop()
