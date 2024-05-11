import tkinter as tk
from tkinter import ttk
import pandas as pd

class FilterBooksPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.data = pd.read_csv('goodreads.csv')
        self.clean_data()
        self.create_widgets()

    def clean_data(self):
        self.data['num_pages'] = pd.to_numeric(self.data['num_pages'], errors='coerce')
        self.data.dropna(subset=['num_pages'], inplace=True)  # Remove rows where 'num_pages' conversion failed
        self.data['num_pages'] = self.data['num_pages'].astype(int)
        self.data['genres'] = self.data['genres'].apply(lambda x: [genre.strip() for genre in x.strip("[]").split(",")])
        self.data = self.data.explode('genres')
        self.data.drop_duplicates(subset='title', keep='first', inplace=True)

    def filter_books(self):
        title_search = self.title_entry.get().lower()
        min_rating = self.rating_combobox.get()
        max_pages = self.pages_combobox.get()
        genre = self.genre_combobox.get()

        filtered = self.data
        try:
            if title_search:
                filtered = filtered[filtered['title'].str.lower().str.contains(title_search)]
            if min_rating != "All":
                filtered = filtered[filtered['rating_score'] >= float(min_rating)]
            if max_pages != "All":
                filtered = filtered[filtered['num_pages'] <= int(max_pages)]
            if genre and genre != "All":
                filtered = filtered[filtered['genres'].str.contains(genre, case=False, na=False)]
            filtered = filtered.sort_values(by='rating_score', ascending=False)
        except ValueError as e:
            print("Error:", e)
            return pd.DataFrame(columns=self.data.columns)  # Return an empty DataFrame on error
        return filtered[['title', 'rating_score', 'num_pages', 'genres']]

    def update_display(self):
        filtered_data = self.filter_books()
        self.result_listbox.delete(0, tk.END)  # Clear previous results
        # Header
        self.result_listbox.insert(tk.END, f"{'Title':<80}{'Rating':<10}{'Pages':<10}{'Genres'}")
        # Data rows
        for index, row in filtered_data.iterrows():
            title = row['title'] if len(row['title']) < 30 else row['title'][:60]
            genres = row['genres'] if len(row['genres']) < 20 else row['genres'][:25]
            list_entry = f"{title:<80}{row['rating_score']:<10}{row['num_pages']:<10}{genres}"
            self.result_listbox.insert(tk.END, list_entry)

    def create_widgets(self):
        ttk.Label(self, text="Search Title:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.title_entry = ttk.Entry(self)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self, text="Minimum Rating:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.rating_combobox = ttk.Combobox(self, values=["All", 3, 3.5, 4, 4.5], state="readonly")
        self.rating_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.rating_combobox.set('All')

        ttk.Label(self, text="Genre:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.genre_combobox = ttk.Combobox(self, values=['All'] + sorted(self.data['genres'].dropna().unique().tolist()), state="readonly")
        self.genre_combobox.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        self.genre_combobox.set('All')

        ttk.Label(self, text="Max Pages:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.pages_combobox = ttk.Combobox(self, values=["All", 100, 300, 500, 1000], state="readonly")
        self.pages_combobox.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        self.pages_combobox.set('All')

        ttk.Button(self, text="Filter Books", command=self.update_display).grid(row=4, column=0, columnspan=2, pady=10)

        # Frame to contain Listbox and Scrollbar
        list_frame = ttk.Frame(self)
        list_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
        self.grid_rowconfigure(5, weight=1)  # Make the list frame expandable
        self.grid_columnconfigure(1, weight=1)  # Allow the Listbox to expand

        # Listbox with a vertical scrollbar
        self.result_listbox = tk.Listbox(list_frame, height=10, width=80, exportselection=0, font=('Courier', 14))
        self.result_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.result_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_listbox.config(yscrollcommand=scrollbar.set)
