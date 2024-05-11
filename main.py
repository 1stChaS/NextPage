import tkinter as tk
from tkinter import ttk
from filter import FilterBooksPage
from book_recommendation import BookRecommendationPage
from data_visualization import DataVisualizationPage
from interesting_data import InterestingDataPage


def show_page(page):
    page.lift()


root = tk.Tk()
root.title("NextPage Book Management System")
root.geometry('1350x600')

# Tabs
tab_control = ttk.Notebook(root)
filter_tab = tk.Frame(tab_control)
recommendation_tab = tk.Frame(tab_control)
interesting_data_tab = tk.Frame(tab_control)
visualization_tab = tk.Frame(tab_control)

tab_control.add(filter_tab, text='Book Filtering')
tab_control.add(recommendation_tab, text='Book Recommendation')
tab_control.add(interesting_data_tab, text='Interesting Data')
tab_control.add(visualization_tab, text='Data Visualization')
tab_control.pack(expand=1, fill="both")

# Filter Page
filter_page = FilterBooksPage(filter_tab)
filter_page.pack(expand=True, fill="both")

# Recommendation Page
recommendation_page = BookRecommendationPage(recommendation_tab)
recommendation_page.pack(expand=True, fill="both")

# interesting data
interesting_data = InterestingDataPage(interesting_data_tab)
interesting_data.pack(expand=True, fill="both")

# Visualization Page
visualization_page = DataVisualizationPage(visualization_tab)
visualization_page.pack(expand=True, fill="both")

# Navigation Buttons
nav_frame = tk.Frame(root)
nav_frame.pack(side="top", fill="x", expand=False)

root.mainloop()