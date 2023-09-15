import os
import tkinter as tk

import numpy as np
import pandas as pd
from pymongo import MongoClient

from inventory_management_system import InventoryMangement


class LoginPage:
    def __init__(self, root):
        self.login_result = False
        self.root = root
        self.invn = InventoryMangement(self.root)
        self.user_info_path = "Data/user_info.csv"

    def exit_tk(self):
        self.root.destroy()

    def detail_check(self, username_entry, password_entry, result_label):
        user_info = pd.read_csv(self.user_info_path)

        entered_username = username_entry.get()
        entered_password = password_entry.get()

        user_identification = user_info[user_info["Username"] == entered_username]

        if (
            user_identification.shape[0] != 0
            and entered_password == user_identification["Password"].iloc[0]
        ):
            root = tk.Toplevel(self.root)
            add_button = tk.Button(
                root,
                text="Add Book",
                command=lambda: self.invn.add_book(),
                width=15,
            )
            add_button.pack(pady=10, side="top", anchor="w", padx=10)

            retrive_button = tk.Button(
                root,
                text="Show Books",
                command=lambda: self.invn.retrieve_books(),
                width=15,
            )
            retrive_button.pack(pady=10, anchor="w", padx=10)

            close_button = tk.Button(root, text="Exit", command=self.exit_tk, width=15)
            close_button.pack(pady=10, anchor="w", padx=10)
        else:
            result_label.config(text="Login Failed")
            self.root.after(5000, lambda: result_label.config(text=""))

    def login_(self):

        username_label = tk.Label(self.root, text="Username:")
        username_label.pack()

        username_entry = tk.Entry(self.root)
        username_entry.pack()

        password_label = tk.Label(self.root, text="Password:")
        password_label.pack()

        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        login_button = tk.Button(
            self.root,
            text="Login",
            command=lambda: self.detail_check(
                username_entry, password_entry, result_label
            ),
        )
        login_button.pack()

        result_label = tk.Label(self.root, text="")
        result_label.pack()

    def add_data(self, name, username, password):
        if not os.path.exists(self.user_info_path):
            # Create a new CSV file with a header row if it doesn't exist
            df = pd.DataFrame(columns=["Name", "Username", "Password"])
            df.to_csv(self.user_info_path, index=False)

        data = {"Name": name, "Username": username, "Password": password}
        user_df = pd.DataFrame([data])
        user_df.to_csv(self.user_info_path, mode="a", header=False, index=False)

        self.child_root.destroy()  # Close the registration window after saving data

    def user_registration(self):

        self.child_root = tk.Toplevel(self.root)
        self.child_root.title("Registration Page")

        label1 = tk.Label(self.child_root, text="Enter Your Name: ")
        label1.pack()

        entry1 = tk.Entry(self.child_root)
        entry1.pack()

        label2 = tk.Label(self.child_root, text="Enter Your Username: ")
        label2.pack()

        entry2 = tk.Entry(self.child_root)
        entry2.pack()

        label3 = tk.Label(self.child_root, text="Enter Your Password: ")
        label3.pack()

        entry3 = tk.Entry(self.child_root)
        entry3.pack()

        submit_button = tk.Button(
            self.child_root,
            text="Submit",
            command=lambda: self.add_data(entry1.get(), entry2.get(), entry3.get()),
        )
        submit_button.pack()
