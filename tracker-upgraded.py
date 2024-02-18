import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import requests


#the window
window= tk.Tk()                                         
window.title("Money Tracker💸")
window.iconbitmap("expenses.ico")
window.geometry("1200x600")
# Create a Style object
style = ttk.Style()

expenses_list=[]

#Main Functionality

def validate_numbers(amount, income):
    try:
        amount= float(entry_amount.get())
        income= float( entry_income.get())
        return amount, income
    except ValueError:
        messagebox.showerror("Error", "Please Enter Just Numbers!")
        return None

def get_date():
    return entry_date.get_date()    
        



def display_expenses(record):
    treeview.insert('', 'end', values=(
        record['income'],
        record['date'],
        record['category'],
        record['amount'],
        record['amount_currency'],
        record['payment_method'],
        ))



def convert_to_usd(amount,income ,amount_currency, income_currency):
    api_key= "24c9f38ded444584902523b5ed1a8da6"
    request_url= f'https://api.currencyfreaks.com/v2.0/rates/latest?apikey={api_key}'

    response = requests.request("GET", request_url)
    result = response.json()
    amount_result= result['rates'][amount_currency]
    amount_usd= round((amount / float(amount_result)),2)

    income_result= result['rates'][income_currency]
    income_usd= round((income / float(income_result)),2)
    return (amount_usd, income_usd)
        
    




def update_total_row():
  
    daily_totals = {}
    for record in expenses_list:
        date = record['date']
       # the amount and income in USD
        amount_usd, income_usd= convert_to_usd(record['amount'], record['income'], record['amount_currency'], record['income_currency'])
        
        if date in daily_totals:
            daily_totals[date]['total'] += amount_usd
            print(amount_usd)
        else:
            daily_totals[date] = {'total': amount_usd, 'income': income_usd} 
            print(income_usd)

 

    # Insert the updated records and totals
    for date, totals in daily_totals.items():
        remains = totals['income'] - totals['total']
        treeview.insert('', 'end', values=("Total", date, "", totals['total'],"USD", "", f"{remains:.2f}"), tags=('total',))

   


def add_expenses():
    #retrieve the valuesfrom the inputs
    amount= entry_amount.get();
    income= entry_income.get();
    amount_currency= combo_currencies.get();
    income_currency= combo_income_currencies.get();
    payment_method=combo_methodPayment.get();
    category = Category_combo.get();
    date = get_date();
   # if the fields are empty
    if not amount or not income or not amount_currency or not income_currency or not category or not payment_method or not date :
      
        messagebox.showwarning("Warning", "All Fields are required")
        return
    
    (amount, income)=validate_numbers(amount, income)
    ##create the expenses ditionary to collect data 
    expenses_record = {
        "amount": amount,
        "income": income,
        "amount_currency":amount_currency,
        "income_currency": income_currency,
        "category":category,
        "payment_method":payment_method,
        "date":date,

    }
    expenses_list.append(expenses_record)

    #Display the data in the tree view
    display_expenses(expenses_record)

   

    #clear the input field
    entry_amount.delete(0, tk.END)
    entry_income.delete(0, tk.END)
    combo_currencies.set("")
    combo_income_currencies.set("")
    Category_combo.set("")
    combo_methodPayment.set("")

    #return the values

    return expenses_record
    

#/////////////////////////////////////////////////////////////////////////////////////////
# creating the labels and the entry widget
#Frame of entries
frame_entry= tk.Frame(window)
frame_entry.grid(row=0, column=0, columnspan=4, sticky="n")


#income entry 
label_income= tk.Label(frame_entry, text="Income of the Month:")
label_income.grid(row=0, column=0 , columnspan=2,  padx=5, pady=5,  sticky="ew")
entry_income= tk.Entry(frame_entry)
entry_income.grid(row=0, column=2, columnspan=2, padx=20, pady=5, sticky="ew")

label_income_currency= tk.Label(frame_entry, text="Income Currency:")
label_income_currency.grid(row=0, column=5 , columnspan=2,  padx=5, pady=5,  sticky="ew")
combo_income_currencies=ttk.Combobox(frame_entry, values=["EGP","USD", "EUR", "GBP"])
combo_income_currencies.grid(row=0, column=7, columnspan=2, padx=5, pady=5, sticky="ew" )



#Amount
label_amount= tk.Label(frame_entry, text="Amount Spent:")
label_amount.grid(row=1, column=0 , columnspan=2,  padx=5, pady=5,  sticky="ew")
entry_amount= tk.Entry(frame_entry)
entry_amount.grid(row=1, column=2, columnspan=2, padx=20, pady=5, sticky="ew")

#currency
label_currency= tk.Label(frame_entry, text="Amount Currency:")
label_currency.grid(row=1, column=5, columnspan=2,  padx=5, pady=5,  sticky="ew")
combo_currencies=ttk.Combobox(frame_entry, values=["EGP","USD", "EUR", "GBP"])
combo_currencies.grid(row=1, column=7, columnspan=2, padx=5, pady=5, sticky="ew" )

#catagory
label_currency= tk.Label(frame_entry, text="Category:")
label_currency.grid(row=3, column=0 , columnspan=2,  padx=5, pady=5,  sticky="ew")
Category_combo=ttk.Combobox(frame_entry, values= ["Daily Expnses", "Shopping", "Internet & phone", "transportation", "Hanging out", "Savings", "Family", "Urgent","Coffee"])
Category_combo.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky="ew" )

#payment 
label_method= tk.Label(frame_entry, text="Payment Method:")
label_method.grid(row=4, column=0 , columnspan=2,  padx=5, pady=5,  sticky="ew")
combo_methodPayment=ttk.Combobox(frame_entry, values= ["Cash", "Visa", "Vodafone Cash", "Online Card","PayPal"])
combo_methodPayment.grid(row=4, column=2, columnspan=2, padx=5, pady=5, sticky="ew" )

#data
label_date= tk.Label(frame_entry, text="Date:")
label_date.grid(row=5, column=0 , columnspan=2,  padx=5, pady=5,  sticky="ew")
entry_date= DateEntry(frame_entry, selectmode="day")
entry_date.grid(row=5, column=2, columnspan=2, padx=5, pady=5, sticky="ew")

#the action buttons 
# Add Button 
button_add= tk.Button(frame_entry, text="Add",height=2, width=12, background="green", foreground="white",  command= add_expenses)
button_add.grid(row=6, column=4, columnspan=2, sticky="e")


# Remaiing Button
button_add= tk.Button(frame_entry, text="Balance",height=2, width=12, background="orangered", foreground="white", command= update_total_row )
button_add.grid(row=6, column=6, columnspan=2, sticky="w", padx= 20)



#the table view 

columns = ('income', 'date', 'category', 'amount','currency', 'payment_method', 'remains')
treeview = ttk.Treeview(window, columns=columns, show='headings')
treeview.grid(row=7, column=0, columnspan=4,padx=50, pady=10, sticky='nsew')

#Styling the treeview
 # Configure row tags for styling
treeview.tag_configure('total', background='yellow')
treeview.tag_configure('remains', foreground='red')


# Configure the style of Treeview Heading
style.configure("Treeview.Heading", font=('Calibri', 10, 'bold'), foreground="blue", background="lightgray")

# Setting column headings
for col in columns:
    treeview.heading(col, text=col.capitalize())
    treeview.column(col, anchor='center',stretch=False, width=150)

# Scrollbar for the Treeview
scrollbar = ttk.Scrollbar(window, orient="vertical", command=treeview.yview)
scrollbar.grid(row=7, column=4, sticky='ns')
treeview.configure(yscrollcommand=scrollbar.set)


window.mainloop()



