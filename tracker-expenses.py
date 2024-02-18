import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import requests


#the window
window= tk.Tk()                                         
window.title("Money Tracker💸")
window.iconbitmap("expenses.ico")
window.geometry("900x500")
style = ttk.Style()


expenses_list=[]

#Main Functionality

def validate_numbers(amount):
    try:
        amount= float(entry_amount.get())
        return amount
    except ValueError:
        messagebox.showerror("Error", "Please Enter Just Numbers!")
        return 

def get_date():
    return entry_date.get_date()    
        



def display_expenses(record):
    treeview.insert('', 'end', values=(
       
        record['date'],
        record['category'],
        record['amount'],
        record['amount_currency'],
        record['payment_method'],
        
        ))


# Using API
def convert_to_usd(amount, currency):
    #Converts an amount from a specified currency into USD.
    api_key= "24c9f38ded444584902523b5ed1a8da6"
    request_url= f'https://api.currencyfreaks.com/v2.0/rates/latest?apikey={api_key}'

    response = requests.request("GET", request_url)
    result = response.json()
    result_currency= result['rates'][currency]
    result_usd= round((amount / float(result_currency)),2)
    return result_usd
    
    



def update_total_row():

   # Remove any existing total row
    for child in treeview.get_children():
        if 'total' in treeview.item(child, 'tags'):
            treeview.delete(child)

#     # Calculate the total expenditures in USD
    total_expenditures = 0
    for record in expenses_list:
       
        amount_in_usd = convert_to_usd(float(record['amount']), record['amount_currency'])
        total_expenditures += amount_in_usd
    
#     # Insert the new total row at the end of the Treeview
#    # When inserting the total row
    treeview.insert('', 'end', values=("Total", "",  total_expenditures, "USD",""), tags=('total',))




def add_expenses():
   
    # Get user input from entry fields
    amount = entry_amount.get()
    amount_currency = combo_currencies.get()
    category = Category_combo.get()
    date = entry_date.get()  # Assuming you are using a DateEntry widget
    payment_method = combo_methodPayment.get()
    
   # if the fields are empty
    if not amount or not amount_currency or not category or not payment_method or not date :
      
        messagebox.showwarning("Warning", "All Fields are required")
        return
    
    amount= validate_numbers(amount)
   
    ##create the expenses ditionary to collect data 
    expenses_record = {
        "amount": amount,
        "amount_currency":amount_currency,   
        "category":category,
        "payment_method":payment_method,
        "date":date,

    }
    expenses_list.append(expenses_record)

    #Display the data in the tree view
    display_expenses(expenses_record)

    #update the expenses in display 
    update_total_row()

    #clear the input field
    entry_amount.delete(0, tk.END)
    combo_currencies.set("")
    Category_combo.set("")
    combo_methodPayment.set("")

    #return the values

    return expenses_record
    



# creating the labels and the entry widget
#Frame of entries
frame_entry= tk.Frame(window)
frame_entry.grid(row=0, column=0, columnspan=4, sticky="n")





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





#the table view 

columns = ('date', 'category', 'amount','currency', 'payment_method')
treeview = ttk.Treeview(window, columns=columns, show='headings')
treeview.grid(row=7, column=0, columnspan=4,padx=50, pady=10, sticky='nsew')

#Styling the treeview



# Configure the style of Treeview Heading
style.configure("Treeview.Heading", font=('Calibri', 10, 'bold'), foreground="blue", background="lightgray")
treeview.tag_configure('total', background='yellow')



# Setting column headings
for col in columns:
    treeview.heading(col, text=col.capitalize())
    treeview.column(col, anchor='center',stretch=False, width=150)

# Scrollbar for the Treeview
scrollbar = ttk.Scrollbar(window, orient="vertical", command=treeview.yview)
scrollbar.grid(row=7, column=4, sticky='ns')
treeview.configure(yscrollcommand=scrollbar.set)


window.mainloop()



