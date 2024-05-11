import tkinter as tk

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import pandas as pd


class InterestingDataPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.df = pd.read_csv('goodreads.csv')
        self.setup_dataframe()  # Prepare data for plotting

        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas_widget = self.canvas.get_tk_widget()

        self.combobox = ttk.Combobox(self, values=[
            "Top Books by Voters and Rating",
            "Distribution of Book Length",
            "Distribution of Book Formats",
            "Number of Voters for Each Book",
            "Distribution of Book Ratings"
        ])
        self.combobox.current(0)
        self.combobox.bind("<<ComboboxSelected>>", self.update_graph)

        self.combobox.pack(fill='x')
        self.canvas_widget.pack(fill='both', expand=True)

        self.update_graph()  # Initial graph

    def setup_dataframe(self):
        # Convert and prepare data as needed for plotting
        self.df['Number of voters'] = pd.to_numeric(self.df['num_ratings'], errors='coerce')
        self.df['Rating'] = pd.to_numeric(self.df['rating_score'], errors='coerce')
        self.df['Num Pages'] = pd.to_numeric(self.df['num_pages'], errors='coerce')
        self.df['Book'] = self.df['title']  # Ensure this column is set up correctly

    def draw_top_books(self):
        top_books = self.df.sort_values(by=['Number of voters', 'Rating'], ascending=False).head(20)
        sns.barplot(x='Number of voters', y='Rating', hue='Book', data=top_books, ax=self.ax)

    def draw_book_length_distribution(self):
        sns.histplot(data=self.df, x='Num Pages', bins=30, kde=True, color='red', ax=self.ax)

    def draw_book_format_distribution(self):
        format_dist = self.df['format'].value_counts()
        sns.barplot(x=format_dist.index, y=format_dist.values, ax=self.ax)

    def draw_voters_per_book(self):
        voters_distributed = self.df.groupby('Book')['Number of voters'].sum().sort_values(ascending=False).head(20)
        self.ax.barh(voters_distributed.index, voters_distributed.values, color='coral')

    def draw_rating_distribution(self):
        books_rating_distribution = self.df['Rating'].value_counts().sort_index()
        sns.barplot(x=books_rating_distribution.index, y=books_rating_distribution.values, ax=self.ax)

    def update_graph(self, event=None):
        self.ax.clear()
        graph_type = self.combobox.get()

        if graph_type == "Top Books by Voters and Rating":
            self.draw_top_books()
        elif graph_type == "Distribution of Book Length":
            self.draw_book_length_distribution()
        elif graph_type == "Distribution of Book Formats":
            self.draw_book_format_distribution()
        elif graph_type == "Number of Voters for Each Book":
            self.draw_voters_per_book()
        elif graph_type == "Distribution of Book Ratings":
            self.draw_rating_distribution()

        self.canvas.draw()

