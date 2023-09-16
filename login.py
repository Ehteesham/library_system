import os
import tkinter as tk

import numpy as np
import pandas as pd

from inventory_management_system import InventoryMangement


class LoginPage:
    def __init__(self, root):
        self.login_result = False
        self.parent_root = root
        self.invn = InventoryMangement(self.parent_root)
        self.user_info_path = "Data/user_info.csv"

    def detail_check(
        self,
        username_entry,
        password_entry,
        result_label,
        lower_frame,
        login_frame,
        book_list_frame,
        lower_left,
    ):
        user_info = pd.read_csv(self.user_info_path)

        entered_username = username_entry.get()
        entered_password = password_entry.get()

        user_identification = user_info[user_info["Username"] == entered_username]

        if (
            user_identification.shape[0] != 0
            and entered_password == user_identification["Password"].iloc[0]
        ):
            add_button = tk.Button(
                lower_frame,
                text="Add Book",
                command=lambda: self.invn.add_book(),
                width=10,
                height=1,
            )
            add_button.pack(pady=5, padx=5, anchor="w")

            retrive_button = tk.Button(
                lower_frame,
                text="Show Books",
                command=lambda: self.invn.retrieve_books(
                    book_list_frame,
                    retrive_button,
                    lower_frame,
                    lower_left,
                ),
                width=10,
                height=1,
            )
            retrive_button.pack(pady=5, padx=5, anchor="w")

            close_button = tk.Button(
                lower_frame,
                text="Exit",
                command=self.parent_root.destroy,
                width=10,
                height=1,
            )
            close_button.pack(pady=5, padx=5, anchor="w")

            self.clear_frame(login_frame)

            login_label = tk.Label(
                login_frame,
                text="Hello",
                width=28,
                height=2,
            )
            login_label.pack()

            self.root.destroy()
        else:
            result_label.config(text="Login Failed")
            self.root.after(3000, lambda: result_label.config(text=""))
            self.root.destroy()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def login_(self, login_frame, lower_frame, book_list_frame, lower_left):
        self.root = tk.Toplevel(self.parent_root)
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
                username_entry,
                password_entry,
                result_label,
                lower_frame,
                login_frame,
                book_list_frame,
                lower_left,
            ),
        )
        login_button.pack()

        result_label = tk.Label(self.root, text="")
        result_label.pack()

    def add_data(self, name, username, password):
        if not os.path.exists(self.user_info_path):
            df = pd.DataFrame(columns=["Name", "Username", "Password"])
            df.to_csv(self.user_info_path, index=False)

        data = {"Name": name, "Username": username, "Password": password}
        user_df = pd.DataFrame([data])
        user_df.to_csv(self.user_info_path, mode="a", header=False, index=False)

        self.child_root.destroy()

    def user_registration(self, login_frame):
        self.child_root = tk.Toplevel(self.parent_root)
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
