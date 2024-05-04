import tkinter as tk

class BookRecommendationPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Book Recommendation System Coming Soon!")
        label.pack(pady=20)

        def getRecommendedItems(prefs, itemMatch, user):
            userRatings = prefs[user]
            scores = {}
            totalSim = {}

