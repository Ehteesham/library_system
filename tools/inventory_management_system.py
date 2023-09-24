import os
import tkinter as tk
from datetime import datetime
from tkinter import font, ttk

import numpy as np
import pandas as pd

from tools.qr_code_handle import QrCodeGenerator
from tools.search_system import SearchSystem


class InventoryMangement:
    def __init__(self, root, book_list_frame, login_frame, lower_right, lower_left):
        self.parent_root = root
        self.upper_left = book_list_frame
        self.login_frame = login_frame
        self.lower_right = lower_right
        self.lower_left = lower_left
        self.qr = QrCodeGenerator(login_frame)
        self.book_info_dir = "D:/CodeClause/Library Management System/Data/books_manegment.csv"
        self.columns = ("Book Name", "Description",
                        "Authors", "Genres", "Date")
        self.book_tree = ttk.Treeview(
            self.upper_left, columns=self.columns, show="headings", height=17
        )
        self.book_info_df = None
        self.book_info = None

    def add_book(self):
        def register_text():
            selected_option = option_var.get()
            entered_text1 = entry1.get()
            entered_text2 = entry2.get()
            entered_text3 = entry3.get()
            entered_text4 = entry4.get()
            date = datetime.now().strftime("%Y %m %d")
            self.book_info = {
                "Book Name": entered_text1,
                "Description": entered_text3,
                "Author Name": entered_text2,
                "Genre": selected_option,
                "Link": entered_text4,
                "Date": date
            }
            self.book_info_df = pd.DataFrame([self.book_info])
            if os.path.isfile(self.book_info_dir):
                saved_df = pd.read_csv(self.book_info_dir)
                merged_df = pd.concat(
                    [saved_df, self.book_info_df], ignore_index=True)
                merged_df.to_csv(self.book_info_dir, index=False)
            else:
                self.book_info_df.to_csv(self.book_info_dir, index=False)
            self.root.destroy()

        self.root = tk.Toplevel(self.parent_root)
        self.root.title("Adding Book")

        label1 = tk.Label(self.root, text="Book Name: ")
        label1.pack()

        entry1 = tk.Entry(self.root)
        entry1.pack()

        label3 = tk.Label(self.root, text="Description: ")
        label3.pack()

        entry3 = tk.Entry(self.root)
        entry3.pack()

        label2 = tk.Label(self.root, text="Author Name: ")
        label2.pack()

        entry2 = tk.Entry(self.root)
        entry2.pack()

        label4 = tk.Label(self.root, text="Link: ")
        label4.pack()

        entry4 = tk.Entry(self.root)
        entry4.pack()

        option_var = tk.StringVar()
        option_var.set("None")

        options = ["Entertainment", "Technology", "Finance"]

        option_menu = tk.OptionMenu(self.root, option_var, *options)
        option_menu.pack()

        print_button = tk.Button(
            self.root, text="Submit", command=register_text)
        print_button.pack()

        self.root.mainloop()

    def search(self):
        sc = SearchSystem(self.parent_root, self.book_tree, self.columns)
        sc.view()

    def retrieve_books(self, retrive_button, Username):
        def limit_text(text, max_chars):
            if len(text) > max_chars:
                return text[:max_chars]
            else:
                return text

        def clear_frame(frame):
            for widget in frame.winfo_children():
                widget.destroy()

        def qr1(book_name):
            book_df = book_df = pd.read_csv(self.book_info_dir, sep=",")
            user_report = book_df[book_df['Book Name'] == book_name]
            self.qr.getqr(book_df, book_name)

        def view_details(text, bold_font):
            clear_frame(self.login_frame)

            text.config(state="normal")

            text.delete(1.0, "end")

            text.tag_configure("bold", font=bold_font)
            name_item = self.book_tree.selection()[0]
            name_value = self.book_tree.item(name_item, "values")[0]

            text.insert("1.0", "Book Name - ", "bold")
            text.insert("1.13", f"{name_value}\n", "normal")

            description_item = self.book_tree.selection()[0]
            description_value = self.book_tree.item(
                description_item, "values")[1]
            limited_text = limit_text(description_value, 850)
            text.insert("2.0", "Description - ", "bold")
            text.insert("2.15", f"{description_value}\n", "normal")

            author_item = self.book_tree.selection()[0]
            author_value = self.book_tree.item(author_item, "values")[2]
            text.insert("3.0", "Author - ", "bold")
            text.insert("3.10", f"{author_value}\n", "normal")

            genre_item = self.book_tree.selection()[0]
            genre_value = self.book_tree.item(genre_item, "values")[3]
            text.insert("4.0", "Genre - ", "bold")
            text.insert("4.8", f"{genre_value}\n", "normal")

            date_item = self.book_tree.selection()[0]
            date_value = self.book_tree.item(date_item, "values")[4]
            text.insert("5.0", "Published Date - ", "bold")
            text.insert("5.17", f"{date_value}\n", "normal")

            text.config(state="disabled")

            self.purchase_button = tk.Button(
                self.lower_right,
                text="Get Book",
                width=10,
                height=1,
                padx=5,
                pady=5,
                command=lambda: qr1(name_value),
            )
            self.purchase_button.grid(row=2, column=1, padx=5, pady=5)

        def update_book_list(tx=None, states=False):
            if states == True:
                for column_id in self.book_tree.get_children():
                    self.book_tree.delete(column_id)
                self.book_tree["columns"] = (
                    "Book Name",
                    "Description",
                    "Author",
                    "Genres",
                    "Date"
                )
                self.book_tree.heading("#1", text="Book Name")
                self.book_tree.column("#1")
                self.book_tree.heading("#2", text="Description")
                self.book_tree.column("#2")
                self.book_tree.heading("#3", text="Author")
                self.book_tree.column("#3")
                self.book_tree.heading("#4", text="Genres")
                self.book_tree.column("#4")
                self.book_tree.heading("#5", text="Date")
                self.book_tree.column("#5")

                tx.config(state="normal")
                tx.delete("1.0", "end")
                book_df = pd.read_csv(self.book_info_dir, sep=",")
                ls = []
                for rows in range(book_df.shape[0]):
                    ls.append(tuple(book_df.iloc[rows]))

                for book in ls:
                    self.book_tree.insert("", "end", values=book)
                self.qr.display_qr(state=True)
            else:
                # self.book_tree.delete(*self.book_tree.get_children())
                book_df = pd.read_csv(self.book_info_dir, sep=",")
                ls = []
                for rows in range(book_df.shape[0]):
                    ls.append(tuple(book_df.iloc[rows]))

                for book in ls:
                    self.book_tree.insert("", "end", values=book)

        text = tk.Text(self.lower_left, wrap="word",
                       bg="white", font=("Arial", 12))
        text.pack(fill="both", expand=True)

        bold_font = font.Font(text, text.cget("font"))
        bold_font.configure(weight="bold")
        self.book_tree.bind(
            "<ButtonRelease-1>",
            lambda event, text=text, bold_font=bold_font: view_details(
                text, bold_font),
        )
        for col in self.columns:
            self.book_tree.heading(col, text=col)
            if col == "Book Name" or col == "Description":
                self.book_tree.column(col, width=305)
            else:
                self.book_tree.column(col, width=120)
        self.book_tree.pack(fill="both", expand=True)
        update_book_list()
        retrive_button.config(
            text="Refresh list", command=lambda: update_book_list(tx=text, states=True)
        )
