import os
import tkinter as tk
from datetime import datetime
from tkinter import ttk

import numpy as np
import pandas as pd


class InventoryMangement:
    def __init__(self, root):
        self.parent_root = root
        self.book_info = None
        self.book_info_dir = "Data/books_manegment.csv"
        self.book_info_df = None

    def add_book(self):
        def register_text():
            selected_option = option_var.get()
            entered_text1 = entry1.get()
            entered_text2 = entry2.get()
            date = datetime.now().strftime("%Y %m %d")
            time = datetime.now().strftime("%I:%M:%S %p")
            self.book_info = {
                "Book Name": entered_text1,
                "Author Name": entered_text2,
                "Genre": selected_option,
                "Date": date,
                "Time": time,
            }
            self.book_info_df = pd.DataFrame([self.book_info])
            if os.path.isfile(self.book_info_dir):
                saved_df = pd.read_csv(self.book_info_dir)
                merged_df = pd.concat([saved_df, self.book_info_df], ignore_index=True)
                merged_df.to_csv(self.book_info_dir, index=False)
            else:
                self.book_info_df.to_csv(self.book_info_dir, index=False)
            self.root.destroy()

        self.root = tk.Toplevel(self.parent_root)
        self.root.title("Adding Book")

        label1 = tk.Label(self.root, text="Enter Book Name: ")
        label1.pack()

        entry1 = tk.Entry(self.root)
        entry1.pack()

        label2 = tk.Label(self.root, text="Enter Author Name: ")
        label2.pack()

        entry2 = tk.Entry(self.root)
        entry2.pack()

        option_var = tk.StringVar()
        option_var.set("None")

        options = ["Entertainment", "Technology", "Finance"]

        option_menu = tk.OptionMenu(self.root, option_var, *options)
        option_menu.pack()

        print_button = tk.Button(self.root, text="Submit", command=register_text)
        print_button.pack()

        self.root.mainloop()

    def retrieve_books(self, book_list_frame, retrive_button, lower_frame):
        def update_book_list():
            for i in book_tree.get_children():
                book_tree.delete(i)

            book_df = pd.read_csv(self.book_info_dir, sep=",")
            ls = []
            for rows in range(book_df.shape[0]):
                ls.append(tuple(book_df.iloc[rows]))

            for book in ls:
                book_tree.insert("", "end", values=book)

        columns = ("Book Name", "Author", "Genre", "Date", "Time")
        book_tree = ttk.Treeview(
            book_list_frame, columns=columns, show="headings", height=15
        )
        for col in columns:
            book_tree.heading(col, text=col)
            book_tree.column(col, width=155)

        book_tree.pack(fill="both", expand=True)
        update_book_list()
        retrive_button.destroy()

        refresh_button = tk.Button(
            lower_frame,
            text="Refresh List",
            command=update_book_list,
            width=15,
            height=2,
        )
        refresh_button.pack(pady=10, side="left", padx=10)
