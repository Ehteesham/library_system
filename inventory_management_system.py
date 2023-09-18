import os
import tkinter as tk
import webbrowser
from datetime import datetime
from tkinter import font, ttk

import numpy as np
import pandas as pd

from qr_code_handle import QrCodeGenerator
from search_system import SearchSystem


class InventoryMangement:
    def __init__(self, root, book_list_frame):
        self.parent_root = root
        self.book_info = None
        self.book_info_dir = "Data/books_manegment.csv"
        self.book_info_df = None
        self.columns = ("Book Name", "Description", "Authors", "Genres", "Date", "Link")
        self.book_tree = ttk.Treeview(
            book_list_frame, columns=self.columns, show="headings", height=17
        )
        self.qr = QrCodeGenerator()

    def add_book(self):
        def register_text():
            selected_option = option_var.get()
            entered_text1 = entry1.get()
            entered_text2 = entry2.get()
            entered_text3 = entry3.get()
            entered_text4 = entry4.get()
            date = datetime.now().strftime("%Y %m %d")
            time = datetime.now().strftime("%I:%M:%S %p")
            self.book_info = {
                "Book Name": entered_text1,
                "Description": entered_text3,
                "Author Name": entered_text2,
                "Genre": selected_option,
                "Link": entered_text4,
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

        print_button = tk.Button(self.root, text="Submit", command=register_text)
        print_button.pack()

        self.root.mainloop()

    def search(self):
        # Assuming you have a Treeview widget named 'book_tree'

        sc = SearchSystem(self.parent_root, self.book_tree, self.columns)
        sc.view()

    def retrieve_books(self, retrive_button, lower_frame, lower_left, login_frame):
        def open_link(event):
            item = self.book_tree.selection()[0]
            link = self.book_tree.item(item, "values")[5]
            if link.startswith("https://") or link.startswith("http://"):
                webbrowser.open(link)

        def limit_text(text, max_chars):
            if len(text) > max_chars:
                return text[:max_chars]
            else:
                return text

        def qrcodehandler(link):
            df = pd.read_csv(self.book_info_dir, sep=",")
            qr_code = df[df["Link"] == link].iloc[:, -1].values[0]
            code = tk.BitmapImage(data=qr_code)
            return code

        def clear_frame(frame):
            for widget in frame.winfo_children():
                widget.destroy()

        def view_details(text, bold_font):
            clear_frame(login_frame)

            text.config(state="normal")
            name_item = self.book_tree.selection()[0]
            name_value = self.book_tree.item(name_item, "values")[0]
            text.delete(1.0, "end")
            text.tag_configure("bold", font=bold_font)
            text.insert("1.0", "Book Name - ", "bold")
            text.insert("1.13", f"{name_value}\n", "normal")

            description_item = self.book_tree.selection()[0]
            description_value = self.book_tree.item(description_item, "values")[1]
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

            link_item = self.book_tree.selection()[0]
            link_value = self.book_tree.item(link_item, "values")[5]
            text.insert("6.0", "Link - ", "bold")
            text.insert("6.8", f"{link_value}\n", "normal")

            text.config(state="disabled")
            code = qrcodehandler(link_value)
            custom_font = font.Font(family="Arial", size=14, weight="bold")
            img_text_label = tk.Label(
                login_frame,
                text="Scan To Get Book",
                wraplength=200,
                font=custom_font,
                bg="white",
            )
            img_text_label.pack()
            img_label = tk.Label(login_frame, image=code, bg="white")
            img_label.pack()
            login_frame.mainloop()

        def update_book_list(tx=None, states=False):
            if states == True:
                tx.config(state="normal")
                tx.delete("1.0", "end")
                self.book_tree.delete(*self.book_tree.get_children())
                book_df = pd.read_csv(self.book_info_dir, sep=",")
                ls = []
                for rows in range(book_df.shape[0]):
                    ls.append(tuple(book_df.iloc[rows]))

                for book in ls:
                    self.book_tree.insert("", "end", values=book)
                self.qr.display_qr(login_frame, state=True)
            else:
                # self.book_tree.delete(*self.book_tree.get_children())
                book_df = pd.read_csv(self.book_info_dir, sep=",")
                ls = []
                for rows in range(book_df.shape[0]):
                    ls.append(tuple(book_df.iloc[rows]))

                for book in ls:
                    self.book_tree.insert("", "end", values=book)

        text = tk.Text(lower_left, wrap="word", bg="white", font=("Arial", 12))
        text.pack(fill="both", expand=True)

        bold_font = font.Font(text, text.cget("font"))
        bold_font.configure(weight="bold")
        self.book_tree.bind("<Double-1>", open_link)
        self.book_tree.bind(
            "<ButtonRelease-1>",
            lambda event, text=text, bold_font=bold_font: view_details(text, bold_font),
        )
        for col in self.columns:
            self.book_tree.heading(col, text=col)
            if col == "Book Name" or col == "Link" or col == "Description":
                self.book_tree.column(col, width=210)
            else:
                self.book_tree.column(col, width=113)
        self.book_tree.pack(fill="both", expand=True)
        update_book_list()
        retrive_button.config(
            text="Refresh list", command=lambda: update_book_list(tx=text, states=True)
        )
