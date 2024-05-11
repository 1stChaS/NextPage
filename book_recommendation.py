import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer


class BookRecommendationPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.data = pd.read_csv('goodreads.csv')
        self.process_data()
        self.create_widgets()
        self.configure_grid()

    def process_data(self):
        # Convert genres to list and explode
        self.data['genres'] = self.data['genres'].apply(
            lambda x: [genre.strip().strip("'") for genre in x.strip("[]").split(",")])
        self.data = self.data.explode('genres')

        # One-hot encode genres
        mlb = MultiLabelBinarizer()
        self.data_genres = self.data.groupby('title')['genres'].agg(set).reset_index()
        self.genre_matrix = mlb.fit_transform(self.data_genres['genres'])

        # Normalize rating score
        self.data['rating_score'] = self.data['rating_score'] / 5.0  # Assuming ratings are out of 5
        ratings = self.data.groupby('title')['rating_score'].mean().values
        # Append ratings as an extra feature
        self.features = np.hstack([self.genre_matrix, ratings[:, None]])

    def create_widgets(self):
        # Search entry and button
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.search_button = ttk.Button(self, text="Search", command=self.search_books)
        self.search_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Listbox to display recommended books
        self.listbox = tk.Listbox(self)
        self.listbox.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    def configure_grid(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)  # Button column less flexible

    def search_books(self):
        book_title = self.search_var.get()
        if book_title:
            recommendations, scores = self.recommend_books(book_title)
            if recommendations:
                self.listbox.delete(0, tk.END)
                for title, score in zip(recommendations, scores):
                    self.listbox.insert(tk.END, f"{title} - Similarity: {score:.2f}")
            else:
                messagebox.showinfo("No Results", "No similar books found. Try another title.")

    def recommend_books(self, book_title, num_recommendations=10):
        try:
            idx = self.data_genres[self.data_genres['title'].str.lower() == book_title.lower()].index[0]
            sim_scores = cosine_similarity(self.features[idx:idx + 1], self.features)[0]
            sim_indices = np.argsort(sim_scores)[::-1][
                          1:num_recommendations + 1]  # Skip the first entry as it is the book itself
            return self.data_genres['title'].iloc[sim_indices].tolist(), sim_scores[sim_indices]
        except IndexError:
            return [], []
