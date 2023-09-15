import os
import tkinter as tk
from datetime import datetime

import numpy as np
import pandas as pd
import pymongo
from pymongo import MongoClient


class InventoryMangement:
    def __init__(self, root):
        self.parent_root = root
        self.book_info = None
        self.book_info_dir = "Data/books_manegment.csv"
        self.book_info_df = None

    def add_book(self):

        self.root = tk.Toplevel(self.parent_root)
        self.root.title("Adding Book")

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
            print(self.book_info)
            self.book_info_df = pd.DataFrame([self.book_info])
            if os.path.isfile(self.book_info_dir):
                self.book_info_df.to_csv(
                    self.book_info_dir, mode="a", index=False, header=False
                )
            else:
                self.book_info_df.to_csv(self.book_info_dir, index=False)
            self.root.destroy()

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

    # def add_book(self):
    #     if self.book_info_dir in os.listdir("Data/"):
    #         df = pd.read_csv(self.book_info_dir)
    #     else:
    #         df = pd.DataFrame()

    #     self.root = tk.Toplevel(self.parent_root)
    #     self.root.title("Adding Book")

    #     def add_and_close(df):
    #         self.get_data()
    #         df_concat = df.append(self.book_info_df, ignore_index=True)
    #         if os.path.isfile(self.book_info_dir):
    #             df_concat.to_csv(
    #                 self.book_info_dir, mode="a", index=False, header=False
    #             )
    #         else:
    #             df_concat.to_csv(self.book_info_dir, index=False)

    #     add_and_close(df)

    def retrieve_books(self):
        def cll_info():
            ls = []

            db = client.library_mang_sys
            infor = db.inventory_management
            num_rows = infor.count_documents({})
            dc_data = list(infor.find({}, projection={"_id": False}))
            ls.append(list(dc_data[0].keys()))

            for i in range(num_rows):
                dc_value = list(dc_data[i].values())
                ls.append(dc_value)

            num_cols = len(dc_data[0])

            recent_book = self.book_info
            if recent_book == None:
                return ls, num_rows, num_cols

            ls.append(list(recent_book.values()))
            return ls, num_rows + 1, num_cols

        def create_table():
            try:
                df = pd.read_csv(self.book_info_dir)
                num_rows, num_cols = df.shape[0], df.shape[1]
                data = np.vstack([df.columns.tolist(), df.values])
            except FileNotFoundError:
                if isinstance(self.book_info_df, pd.core.frame.DataFrame):
                    column_names = self.book_info_df.columns.tolist()
                    data_values = self.book_info_df.values
                    data = np.vstack([column_names, data_values])
                    num_rows, num_cols = (
                        self.book_info_df.shape[0],
                        self.book_info_df.shape[1],
                    )
                else:
                    result_label = tk.Label(self.root, text="No Books are Available")
                    result_label.pack()
                    return

            for i in range(num_rows + 1):
                for j in range(num_cols):
                    cell_value = data[i][j]
                    cell_label = tk.Label(
                        self.root,
                        text=cell_value,
                        width=23,
                        height=2,
                        relief="solid",
                        font=("Comic Sans MS", 11, "bold"),
                    )
                    cell_label.grid(row=i, column=j)

        self.root = tk.Toplevel(self.parent_root)
        # self.root.geometry("700x350")
        self.root.title("List of Books")
        if not cll_info:
            print("Library is Empty!!!!")
        create_table()
