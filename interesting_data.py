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
        self.setup_dataframe()

        self.fig, self.ax = plt.subplots(figsize=(8, 6))  # Smaller figure size adjusted as before
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas_widget = self.canvas.get_tk_widget()

        self.combobox = ttk.Combobox(self, values=[
            "Top Books by Voters and Rating",
            "Distribution of Book Length",
            "Distribution of Book Formats",
            "Top 10 Rated Books",
            "Average ratings of the books of the Top 20 authors"
        ])
        self.combobox.current(0)
        self.combobox.bind("<<ComboboxSelected>>", self.update_graph)
        # Packing and layout code remains the same

        # Pack the combobox first to ensure it stays at the top
        self.combobox.pack(fill='x', padx=10, pady=10)  # Padding for visual spacing

        # Pack the canvas widget next, allowing it to expand and fill the space below the combobox
        self.canvas_widget.pack(fill='both', expand=True, pady=10)  # Added padding for visual separation

        self.update_graph()  # Initial graph


    def setup_dataframe(self):
        # Convert and prepare data as needed for plotting
        self.df['Number of voters'] = pd.to_numeric(self.df['num_ratings'], errors='coerce')
        self.df['Rating'] = pd.to_numeric(self.df['rating_score'], errors='coerce')
        self.df['Num Pages'] = pd.to_numeric(self.df['num_pages'], errors='coerce')
        self.df['Book'] = self.df['title']  # Ensure this column is set up correctly

    def prepare_book_format_data(self):
        # Calculate the total counts and percentages
        format_counts = self.df['format'].value_counts()
        total = format_counts.sum()
        percentages = (format_counts / total) * 100

        # Identify small categories and sum them into 'Others'
        small_categories = percentages < 3
        others_sum = format_counts[small_categories].sum()

        # Drop small categories and add 'Others'
        format_counts = format_counts[~small_categories]
        if others_sum > 0:
            format_counts['Others'] = others_sum

        return format_counts

    def draw_book_format_distribution(self):
        format_counts = self.prepare_book_format_data()
        self.ax.clear()  # Clear existing plots
        wedges, texts, autotexts = self.ax.pie(format_counts, labels=format_counts.index, autopct='%1.1f%%',
                                               startangle=140)

        # Customize wedge properties
        for text, autotext in zip(texts, autotexts):
            if text.get_text() == 'Others':
                autotext.set_color('black')
                autotext.set_weight('bold')
                autotext.set_style('italic')

        self.ax.set_title('Pie Chart of Book Formats')
        self.canvas.draw()

    def draw_top_books(self):
        # Scale the 'Number of voters' by dividing by 10,000 for better visualization scale
        self.df['Scaled Voters'] = self.df['Number of voters'] / 10000

        # Sorting data and selecting top 20 books
        top_books = self.df.sort_values(by=['Scaled Voters', 'Rating'], ascending=False).head(20)

        # Plotting using seaborn
        barplot = sns.barplot(x='Scaled Voters', y='Book', data=top_books, hue='Book', dodge=False, ax=self.ax)

        # Adding text annotations directly on the bars
        for p in barplot.patches:
            width = p.get_width()  # Get the width of each bar
            self.ax.text(width + 0.1,  # Set the text at 0.1 units right of the bar
                         p.get_y() + p.get_height() / 2,  # Get the Y position of the text
                         '{:1.2f}'.format(width),  # Format the number with 2 decimal places
                         ha='left',  # Horizontal alignment
                         va='center')  # Vertical alignment

        self.ax.set_title('Top Books by Voters and Rating')
        self.ax.set_xlabel('Number of Voters (x10,000)')
        self.ax.set_ylabel('Books')

    def draw_book_length_distribution(self):
        sns.histplot(data=self.df, x='Num Pages', bins=30, kde=True, color='red', ax=self.ax)
        self.ax.set_title('Distribution of Book Length')

    def draw_top10_rated_books(self):
        # Assume you have prepared 'top10_books' with the necessary data
        top10_books = self.df.nlargest(10, 'Rating')
        self.ax.clear()
        barplot = sns.barplot(x='Book', y='Rating', data=top10_books, ax=self.ax, palette="viridis")
        self.ax.set_title('Top 10 Rated Books')
        self.ax.set_xlabel('Book Title')
        self.ax.set_ylabel('Rating')
        for p in barplot.patches:
            self.ax.text(p.get_x() + p.get_width() / 2., p.get_height(), f'{p.get_height():.2f}',
                         ha='center', va='bottom')
        self.ax.tick_params(axis='x', rotation=45)

    def draw_top20_authors_by_average_rating(self):
        author_ratings = self.df.groupby('authors')['Rating'].mean().nlargest(20)
        self.ax.clear()
        author_ratings.plot(kind='bar', ax=self.ax, colormap='summer')
        self.ax.set_title('Top 20 Authors by Average Book Rating')
        self.ax.set_xlabel('Author Name')
        self.ax.set_ylabel('Average Rating')
        self.ax.tick_params(axis='x', rotation=45)

    def update_graph(self, event=None):
        self.ax.clear()
        graph_type = self.combobox.get()

        if graph_type == "Top Books by Voters and Rating":
            self.draw_top_books()
        elif graph_type == "Distribution of Book Length":
            self.draw_book_length_distribution()
        elif graph_type == "Distribution of Book Formats":
            self.draw_book_format_distribution()
        elif graph_type == "Top 10 Rated Books":
            self.draw_top10_rated_books()
        elif graph_type == "Average ratings of the books of the Top 20 authors":
            self.draw_top20_authors_by_average_rating()

        self.fig.tight_layout()
        self.canvas.draw()




