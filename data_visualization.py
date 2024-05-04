import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

class DataVisualizationPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.data = pd.read_csv('goodreads.csv')
        self.selected_attribute1 = tk.StringVar()
        self.selected_attribute2 = tk.StringVar()
        self.selected_graph_type = tk.StringVar()
        self.create_widgets()
        self.initialize_graph()

    def create_widgets(self):
        # Set up comboboxes and labels in a single row for better layout
        ttk.Label(self, text="First Attribute:").grid(row=0, column=0, padx=10, pady=5)
        self.attribute_combobox1 = ttk.Combobox(self, textvariable=self.selected_attribute1,
                                                values=["rating_score", "num_ratings", "current_readers", "want_to_read", "price"],
                                                state="readonly")
        self.attribute_combobox1.grid(row=0, column=1, padx=10, pady=5)
        self.attribute_combobox1.set("rating_score")

        ttk.Label(self, text="Second Attribute:").grid(row=0, column=2, padx=10, pady=5)
        self.attribute_combobox2 = ttk.Combobox(self, textvariable=self.selected_attribute2,
                                                values=["rating_score", "num_ratings", "current_readers", "want_to_read", "price"],
                                                state="readonly")
        self.attribute_combobox2.grid(row=0, column=3, padx=10, pady=5)
        self.attribute_combobox2.set("num_ratings")

        ttk.Label(self, text="Graph Type:").grid(row=0, column=4, padx=10, pady=5)
        self.graph_type_combobox = ttk.Combobox(self, textvariable=self.selected_graph_type,
                                                values=["Scatter Plot", "Heat Map"],
                                                state="readonly")
        self.graph_type_combobox.grid(row=0, column=5, padx=10, pady=5)
        self.graph_type_combobox.bind("<<ComboboxSelected>>", self.update_graph)
        self.graph_type_combobox.set("Scatter Plot")

        # Frame for statistics display
        self.stats_frame = ttk.LabelFrame(self, text="Statistic Data")
        self.stats_frame.grid(row=1, column=6, padx=10, pady=10, sticky='ns')

        # Frame for the matplotlib figure
        self.fig_frame = ttk.Frame(self)
        self.fig_frame.grid(row=1, column=0, columnspan=6, padx=10, pady=10, sticky='nsew')
        # self.initialize_graph()

    def initialize_graph(self):
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.fig_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_graph(self, event=None):
        # Clear the axes and any existing content completely, including legends
        self.ax.clear()
        if self.ax.get_legend():
            self.ax.get_legend().remove()
        graph_type = self.selected_graph_type.get()

        if graph_type == "Scatter Plot":
            self.draw_scatter_plot()
        elif graph_type == "Heat Map":
            self.draw_heat_map()

        self.canvas.draw_idle()  # Efficiently redraw the canvas with the new graph
        self.update_statistics()

    def draw_scatter_plot(self):
        x = self.selected_attribute1.get()
        y = self.selected_attribute2.get()
        self.data.plot(kind='scatter', x=x, y=y, ax=self.ax, label=f"{x} vs {y}")
        self.ax.set_title(f'Scatter Plot of {x} vs {y}')
        self.ax.legend()  # Add legend dynamically

    def draw_heat_map(self):
        corr = self.data[[self.selected_attribute1.get(), self.selected_attribute2.get()]].corr()
        sns.heatmap(corr, annot=True, fmt=".4f", ax=self.ax, cmap='coolwarm')
        self.ax.set_title('Heat Map Showing Correlation')

    def update_statistics(self):
        # Clear previous statistics
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        attribute1 = self.selected_attribute1.get()
        attribute2 = self.selected_attribute2.get()

        # Compute and display statistics
        stats1 = self.data[attribute1].describe().apply(lambda x: f"{x:.4f}")
        stats2 = self.data[attribute2].describe().apply(lambda x: f"{x:.4f}")

        ttk.Label(self.stats_frame, text=f"{attribute1} Statistics:\n{stats1}", justify=tk.LEFT).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        ttk.Label(self.stats_frame, text=f"{attribute2} Statistics:\n{stats2}", justify=tk.LEFT).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
