
import json
import tkinter as tk
from tkinter import messagebox

class BankAccount:

    File_bank_account = "bank_account.json"

    def __init__(self, account_name=None, account_password=None):
        self.account_name = account_name
        self.account_password = account_password

    def json_read_file_bank_account(self):
        
        try:
            with open(self.File_bank_account, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def json_write_file_bank_account(self, data):
        
        with open(self.File_bank_account, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def create_bank_account(self, account_name, account_password):
        user_account_data = self.json_read_file_bank_account()

        if account_name in user_account_data:
            print("This account name already exists. Please choose a different one.")
            return

        user_account_data[account_name] = {"Password": account_password, "Bank Amount": 0}
        self.json_write_file_bank_account(user_account_data)

        print(f"Welcome Mr/Mrs {account_name}. Your bank account has been created.")


    def account_log_in(self, account_name, account_password):
        
        user_account_data = self.json_read_file_bank_account()

        if account_name in user_account_data and user_account_data[account_name]["Password"] == account_password:
            print(f"Welcome Mr/Mrs {account_name}.")
            return account_name
        else:
            print("Unknown Account Name or Incorrect Password. Please try again...")
            return None

    def deposit_amount(self, account_name, amount):
        
        user_account_data = self.json_read_file_bank_account()
        if account_name in user_account_data:
            user_account_data[account_name]["Bank Amount"] += amount
            self.json_write_file_bank_account(user_account_data)
            print(f"Success! {amount} $ has been deposited to your account.")
        else:
            print("Account not found!")

    def withdraw_amount(self, account_name, amount):
        
        user_account_data = self.json_read_file_bank_account()
        if account_name in user_account_data:
            if user_account_data[account_name]["Bank Amount"] >= amount:
                user_account_data[account_name]["Bank Amount"] -= amount
                self.json_write_file_bank_account(user_account_data)
                print(f"Success! {amount} $ has been withdrawn from your account.")
            else:
                print("Insufficient funds!")
        else:
            print("Account not found!")

    def show_account_info(self, account_name):
        
        user_account_data = self.json_read_file_bank_account()

        if account_name in user_account_data:
            print("\n--- Account Information ---")
            print(f"Account Name: {account_name}")
            print(f"Bank Amount: {user_account_data[account_name]['Bank Amount']} $")
        else:
            print("Account not found!")

    def get_balance(self, account_name):
        
        user_account_data = self.json_read_file_bank_account()
        if account_name in user_account_data:
            return user_account_data[account_name]["Bank Amount"]
        return 0 
    

bank = BankAccount()

def login():
    
    global logged_in_user
    username = entry_username.get()
    password = entry_password.get()

    if bank.account_log_in(username, password):
        logged_in_user = username  # Kullanıcı adını kaydet
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        open_bank_window()
    else:
        messagebox.showerror("Login Failed", "Unknown Account Name or Incorrect Password. Please try again...")

def create_account():
    
    username = entry_username.get()
    password = entry_password.get()
    if username and password:
        bank.create_bank_account(username, password)
    else:
        messagebox.showerror("Error", "Username and password cannot be empty!")

def open_bank_window():
    
    bank_window = tk.Toplevel(root)
    bank_window.title("Bank Operations")
    bank_window.geometry("400x300")

    global logged_in_user
    balance_label = tk.Label(bank_window, text=f"Amount: {bank.get_balance(logged_in_user)} $", font=("Arial", 14))
    balance_label.pack()

    def update_balance():
        
        balance_label.config(text=f"Amount: {bank.get_balance(logged_in_user)} $")

    def deposit():
        
        try:
            amount = float(entry_deposit.get())
            bank.deposit_amount(logged_in_user, amount)
            update_balance()
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount!")

    def withdraw():
        
        try:
            amount = float(entry_withdraw.get())
            bank.withdraw_amount(logged_in_user, amount)
            update_balance()
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount!")

    tk.Label(bank_window, text="Deposit Amount:").pack()
    entry_deposit = tk.Entry(bank_window)
    entry_deposit.pack()
    btn_deposit = tk.Button(bank_window, text="Deposit", command=deposit)
    btn_deposit.pack()

    tk.Label(bank_window, text="Withdraw Amount:").pack()
    entry_withdraw = tk.Entry(bank_window)
    entry_withdraw.pack()
    btn_withdraw = tk.Button(bank_window, text="Withdraw", command=withdraw)
    btn_withdraw.pack()


root = tk.Tk()
root.title("Bank Account")
root.geometry("400x300")

tk.Label(root, text="Account Name:").pack()
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Password:").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

btn_login = tk.Button(root, text="Login", command=login)
btn_login.pack()

btn_create_account = tk.Button(root, text="Create Account", command=create_account)
btn_create_account.pack()

root.mainloop()
    

                                        

