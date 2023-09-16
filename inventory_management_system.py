import os
import tkinter as tk
import webbrowser
from datetime import datetime
from tkinter import font, ttk

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

    def retrieve_books(self, book_list_frame, retrive_button, lower_frame, lower_left):
        def open_link(event):
            item = book_tree.selection()[0]
            link = book_tree.item(item, "values")[5]
            if link.startswith("https://") or link.startswith("http://"):
                webbrowser.open(link)

        def limit_text(text, max_chars):
            if len(text) > max_chars:
                return text[:max_chars]
            else:
                return text

        def view_details(text, bold_font):
            name_item = book_tree.selection()[0]
            name_value = book_tree.item(name_item, "values")[0]
            text.delete(1.0, "end")
            text.tag_configure("bold", font=bold_font)
            text.insert("1.0", "Book Name - ", "bold")
            text.insert("1.13", f"{name_value}\n", "normal")

            description_item = book_tree.selection()[0]
            description_value = book_tree.item(description_item, "values")[1]
            limited_text = limit_text(description_value, 850)
            text.insert("2.0", "Description - ", "bold")
            text.insert("2.15", f"{description_value}\n", "normal")

            author_item = book_tree.selection()[0]
            author_value = book_tree.item(author_item, "values")[2]
            text.insert("3.0", "Author - ", "bold")
            text.insert("3.10", f"{author_value}\n", "normal")

            genre_item = book_tree.selection()[0]
            genre_value = book_tree.item(genre_item, "values")[3]
            text.insert("4.0", "Genre - ", "bold")
            text.insert("4.8", f"{genre_value}\n", "normal")

            date_item = book_tree.selection()[0]
            date_value = book_tree.item(date_item, "values")[4]
            text.insert("5.0", "Published Date - ", "bold")
            text.insert("5.17", f"{date_value}\n", "normal")

            link_item = book_tree.selection()[0]
            link_value = book_tree.item(link_item, "values")[5]
            text.insert("6.0", "Link - ", "bold")
            text.insert("6.8", f"{link_value}\n", "normal")

        def update_book_list():
            for i in book_tree.get_children():
                book_tree.delete(i)

            book_df = pd.read_csv(self.book_info_dir, sep=",")
            ls = []
            for rows in range(book_df.shape[0]):
                ls.append(tuple(book_df.iloc[rows]))

            for book in ls:
                book_tree.insert("", "end", values=book)

        columns = ("Book Name", "Description", "Authors", "Genres", "Date", "Link")
        book_tree = ttk.Treeview(
            book_list_frame, columns=columns, show="headings", height=17
        )

        text = tk.Text(lower_left, wrap="word", bg="white", font=("Arial", 12))
        text.pack(fill="both", expand=True)

        bold_font = font.Font(text, text.cget("font"))
        bold_font.configure(weight="bold")

        book_tree.bind("<Double-1>", open_link)
        book_tree.bind(
            "<ButtonRelease-1>",
            lambda event, text=text, bold_font=bold_font: view_details(text, bold_font),
        )

        for col in columns:
            book_tree.heading(col, text=col)
            if col == "Book Name" or col == "Link" or col == "Description":
                book_tree.column(col, width=210)
            else:
                book_tree.column(col, width=113)
        book_tree.pack(fill="both", expand=True)
        update_book_list()
        retrive_button.config(text="Refresh list", command=update_book_list)
