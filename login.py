import os
import tkinter as tk
from tkinter import font

import numpy as np
import pandas as pd

from inventory_management_system import InventoryMangement


class LoginPage:
    def __init__(self, root, book_list_frame):
        self.login_result = False
        self.parent_root = root
        self.invn = InventoryMangement(self.parent_root, book_list_frame)
        self.user_info_path = "Data/user_info.csv"

    def detail_check(
        self,
        username_entry,
        password_entry,
        result_label,
        lower_frame,
        login_frame,
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
            self.clear_frame(lower_frame)
            add_button = tk.Button(
                lower_frame,
                text="Add Book",
                command=lambda: self.invn.add_book(),
                width=10,
                height=1,
                padx=5,
                pady=5,
            )

            retrive_button = tk.Button(
                lower_frame,
                text="Show Books",
                command=lambda: self.invn.retrieve_books(
                    retrive_button,
                    lower_frame,
                    lower_left,
                ),
                width=10,
                height=1,
                padx=5,
                pady=5,
            )

            close_button = tk.Button(
                lower_frame,
                text="Exit",
                command=self.parent_root.destroy,
                width=10,
                height=1,
                padx=5,
                pady=5,
            )

            search_button = tk.Button(
                lower_frame,
                text="Search",
                command=self.invn.search,
                width=10,
                height=1,
                padx=5,
                pady=5,
            )

            add_button.grid(row=0, column=0, padx=5, pady=5)
            retrive_button.grid(row=1, column=0, padx=5, pady=5)
            close_button.grid(row=2, column=0, padx=5, pady=5)
            search_button.grid(row=0, column=1, padx=5, pady=5)

            self.clear_frame(login_frame)

            login_label = tk.Label(
                login_frame,
                text="Hello",
                width=28,
                height=2,
            )
            login_label.pack()

        else:
            result_label.config(text="Login Failed")
            lower_frame.after(3000, lambda: result_label.config(text=""))

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def login_(self, login_frame, lower_frame, lower_left):
        bold_font = font.Font(family="Arial", size=12, weight="bold")
        light_font = font.Font(family="Arial", size=10, weight="normal")
        username_label = tk.Label(
            lower_frame, text="Username", bg="white", font=bold_font
        )
        username_label.pack()

        username_entry = tk.Entry(lower_frame, font=light_font)
        username_entry.pack()

        password_label = tk.Label(
            lower_frame, text="Password", bg="white", font=bold_font
        )
        password_label.pack()

        password_entry = tk.Entry(lower_frame, show="*")
        password_entry.pack()

        login_button = tk.Button(
            lower_frame,
            text="Login",
            command=lambda: self.detail_check(
                username_entry,
                password_entry,
                result_label,
                lower_frame,
                login_frame,
                lower_left,
            ),
            width=15,
            pady=5,
        )
        login_button.pack(pady=10)

        result_label = tk.Label(lower_frame, text="", bg="white")
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
