import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BookRecommendationPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.data = pd.read_csv('goodreads.csv')
        self.process_data()
        self.create_widgets()
        self.configure_layout()

    def process_data(self):
        self.data['genres'] = self.data['genres'].apply(
            lambda x: [genre.strip().strip("'") for genre in x.strip("[]").split(",")])
        self.data = self.data.explode('genres')

        mlb = MultiLabelBinarizer()
        self.data_genres = self.data.groupby('title')['genres'].agg(set).reset_index()
        self.genre_matrix = mlb.fit_transform(self.data_genres['genres'])

        self.data['rating_score'] = self.data['rating_score'] / 5.0
        ratings = self.data.groupby('title')['rating_score'].mean().values
        self.features = np.hstack([self.genre_matrix, ratings[:, None]])

    def create_widgets(self):
        self.paned_window = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.left_panel = ttk.Frame(self.paned_window, width=400, height=400)
        self.right_panel = ttk.Frame(self.paned_window, width=400, height=400)
        self.paned_window.add(self.left_panel, weight=1)
        self.paned_window.add(self.right_panel, weight=1)

        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.left_panel)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.book_combobox = ttk.Combobox(self.right_panel, state="readonly")
        self.book_combobox.pack(fill=tk.X, padx=10, pady=10)
        self.book_combobox.bind("<<ComboboxSelected>>", self.display_book_info)

        # Setting up a scrollable frame for the book details
        self.detail_frame = ttk.Frame(self.right_panel)
        self.canvas_details = tk.Canvas(self.detail_frame)
        self.scrollbar = ttk.Scrollbar(self.detail_frame, orient="vertical", command=self.canvas_details.yview)
        self.scrollable_frame = ttk.Frame(self.canvas_details)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas_details.configure(
                scrollregion=self.canvas_details.bbox("all")
            )
        )
        self.canvas_details.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas_details.configure(yscrollcommand=self.scrollbar.set)

        self.canvas_details.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.detail_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Search bar frame
        self.search_frame = ttk.Frame(self.left_panel)
        self.search_frame.pack(fill=tk.X, padx=10, pady=5)

        self.search_label = ttk.Label(self.search_frame, text="Search Title:")
        self.search_label.pack(side=tk.LEFT, padx=(10, 2))

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 10))

        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.search_books)
        self.search_button.pack(side=tk.LEFT, padx=(2, 10))

    def configure_layout(self):
        self.pack(fill=tk.BOTH, expand=True)

    def search_books(self):
        book_title = self.search_var.get()
        if book_title:
            recommendations, scores = self.recommend_books(book_title)
            if recommendations:
                self.plot_recommendations(recommendations, scores)
                self.book_combobox['values'] = recommendations
                self.book_combobox.set('')
                for widget in self.scrollable_frame.winfo_children():
                    widget.destroy()
            else:
                messagebox.showinfo("No Results", "No similar books found. Try another title.")

    def recommend_books(self, book_title, num_recommendations=10):
        try:
            idx = self.data_genres[self.data_genres['title'].str.lower() == book_title.lower()].index[0]
            sim_scores = cosine_similarity(self.features[idx:idx + 1], self.features)[0]
            sim_indices = np.argsort(sim_scores)[::-1][1:num_recommendations + 1]
            return self.data_genres['title'].iloc[sim_indices].tolist(), sim_scores[sim_indices]
        except IndexError:
            return [], []

    def plot_recommendations(self, recommendations, scores):
        self.ax.clear()
        self.ax.scatter(range(len(scores)), scores, picker=False)
        self.ax.set_ylabel('Similarity Score')
        self.ax.set_xticks(range(len(recommendations)))
        self.ax.set_xticklabels(recommendations, rotation=45, ha="right")

        # Annotating each point with its score
        for i, (rec, score) in enumerate(zip(recommendations, scores)):
            self.ax.annotate(f'{score:.2f}', (i, score), textcoords="offset points", xytext=(0, 10), ha='center')

        self.fig.tight_layout()
        self.canvas.draw()

    def display_book_info(self, event=None):
        book_title = self.book_combobox.get()
        if book_title:
            book_data = self.data[self.data['title'].str.lower() == book_title.lower()].iloc[0]
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            labels = [
                f"Title: {book_data['title']}",
                f"Author: {book_data['authors']}",
                f"Series: {book_data['series_title']}, Release #{book_data['series_release_number']}",
                f"Publisher: {book_data['publisher']}",
                f"Language: {book_data['language']}",
                f"Number of Pages: {book_data['num_pages']}",
                f"Format: {book_data['format']}",
                f"Genres: {book_data['genres']}",
                f"Publication Date: {book_data['publication_date']}",
                f"Rating: {book_data['rating_score'] * 5:.1f}/5",
                f"Number of Ratings: {book_data['num_ratings']}",
                f"Number of Reviews: {book_data['num_reviews']}",
                f"Current Readers: {book_data['current_readers']}",
                f"Want to Read: {book_data['want_to_read']}",
                f"Price: {book_data['price']}",
                f"Description: {book_data['description']}"
            ]
            for label_text in labels:
                if "nan" not in label_text:
                    label = ttk.Label(self.scrollable_frame, text=label_text, wraplength=500, justify="left")
                    label.pack(fill='x', padx=5, pady=1, anchor='w')
                    label.pack(fill=tk.BOTH, expand=True)

