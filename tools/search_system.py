import difflib
import string
import tkinter as tk

import nltk
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SearchSystem:
    def __init__(self, root, book_tree, columns):
        self.book_dir = (
            "D:/CodeClause/Library Management System/Data/books_manegment.csv"
        )
        self.book_tree = book_tree
        self.columns = columns
        self.parent_root = root

    def read_book(self):
        df = pd.read_csv(self.book_dir)
        df.fillna(" ", axis=1, inplace=True)
        return df

    def pre_processing(self, user_input):
        def make_tree(book_df):
            self.book_tree.delete(*self.book_tree.get_children())
            ls = []
            for rows in range(book_df.shape[0]):
                ls.append(tuple(book_df.iloc[rows]))

            for book in ls:
                self.book_tree.insert("", "end", values=book)

        def preprocess_text(text):
            text = text.lower()
            text = text.translate(str.maketrans("", "", string.punctuation))
            tokens = word_tokenize(text)
            return " ".join(tokens)

        def search_books(query, num_results=30):
            query_vector = tfidf_vectorizer.transform([preprocess_text(query)])

            similarity_scores = cosine_similarity(query_vector, tfidf_matrix)

            top_indices = similarity_scores.argsort()[0][::-1][:num_results]
            return top_indices

        df = self.read_book()
        df_ = df.copy()
        df["Book Name"] = df["Book Name"].apply(preprocess_text)
        df["Authors"] = df["Authors"].apply(preprocess_text)
        df["Description"] = df["Description"].apply(preprocess_text)

        df["Combined_Text"] = (
            df["Book Name"] + " " + df["Authors"] + " " + df["Description"]
        )

        tfidf_vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf_vectorizer.fit_transform(df["Combined_Text"])

        word_search = user_input.get()
        result = search_books(word_search)
        make_tree(df_.iloc[result])
        self.root.destroy()

    def view(self):
        self.root = tk.Toplevel(self.parent_root)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the X and Y coordinates for the centered window
        x = (screen_width - 200) // 2
        y = (screen_height - 80) // 2

        # Set the window geometry
        self.root.geometry(f"{200}x{80}+{x}+{y}")
        label2 = tk.Label(self.root, text="Enter Book Name")
        label2.pack()

        entry2 = tk.Entry(self.root)
        entry2.pack()

        search_button = tk.Button(
            self.root,
            text="Search",
            command=lambda: self.pre_processing(entry2),
            width=10,
            height=1,
            padx=5,
            pady=5
        )
        search_button.pack(padx=5, pady=5)
