import json
import os
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog

# ---------------- Movie Class ----------------
class Movie:
    def __init__(self, title, director, year, rating):
        self.title = title
        self.director = director
        self.year = year
        self.rating = rating

    def to_dict(self):
        return {
            "title": self.title,
            "director": self.director,
            "year": self.year,
            "rating": self.rating
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["director"], data["year"], data["rating"])

# ---------------- File Handling ----------------
folder = "movies"
os.makedirs(folder, exist_ok=True)

def get_file(title):
    return os.path.join(folder, title.lower().replace(" ", "_") + ".json")

# ---------------- Functions ----------------
def add_movie_gui():
    title = title_entry.get()
    director = director_entry.get()
    year = year_entry.get()
    rating = rating_entry.get()

    if not title or not director or not year or not rating:
        messagebox.showwarning("Missing Info", "Please fill all fields.")
        return

    movie = Movie(title, director, year, rating)
    file_name = get_file(title)
    with open(file_name, "w") as file:
        json.dump(movie.to_dict(), file, indent=2)
    messagebox.showinfo("Success", f"Movie '{title}' added successfully.")

def show_movie_gui():
    title = simpledialog.askstring("Search Movie", "Enter movie title:")
    if not title:
        return
    file_name = get_file(title)
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            data = json.load(file)
            info = f"🎬 Title: {data['title']}\n🎬 Director: {data['director']}\n📅 Year: {data['year']}\n⭐ Rating: {data['rating']}"
            messagebox.showinfo("Movie Info", info)
    else:
        messagebox.showerror("Not Found", "Movie not found!")

def list_movies_gui():
    files = os.listdir(folder)
    if not files:
        messagebox.showinfo("No Movies", "No movies found!")
        return
    movie_list = "\n".join(file.replace(".json", "").replace("_", " ").title() for file in files)
    messagebox.showinfo("Movie List", movie_list)

def delete_movie_gui():
    title = simpledialog.askstring("Delete Movie", "Enter movie title to delete:")
    if not title:
        return
    file_name = get_file(title)
    if os.path.exists(file_name):
        os.remove(file_name)
        messagebox.showinfo("Deleted", f"Movie '{title}' deleted successfully.")
    else:
        messagebox.showerror("Error", "Movie not found!")

# ---------------- GUI Layout ----------------
app = tb.Window(themename="superhero")
app.title("🎬 Movie Manager")

#  Enable Fullscreen
app.attributes("-fullscreen", True)

# 🔁 Escape key to exit fullscreen
def toggle_fullscreen(event=None):
    app.attributes("-fullscreen", False)

app.bind("<Escape>", toggle_fullscreen)

# Title
tb.Label(app, text="🎬 Movie Title", font=("Segoe UI", 14)).pack(pady=5)
title_entry = tb.Entry(app, width=50, bootstyle="info")
title_entry.pack()

# Director
tb.Label(app, text="🎬 Director", font=("Segoe UI", 14)).pack(pady=5)
director_entry = tb.Entry(app, width=50, bootstyle="info")
director_entry.pack()

# Year
tb.Label(app, text="📅 Year", font=("Segoe UI", 14)).pack(pady=5)
year_entry = tb.Entry(app, width=50, bootstyle="info")
year_entry.pack()

# Rating
tb.Label(app, text="⭐ Rating", font=("Segoe UI", 14)).pack(pady=5)
rating_entry = tb.Entry(app, width=50, bootstyle="info")
rating_entry.pack()

# Buttons
tb.Button(app, text="➕ Add Movie", command=add_movie_gui, bootstyle="success", width=30).pack(pady=8)
tb.Button(app, text="🔍 Show Movie", command=show_movie_gui, bootstyle="primary", width=30).pack()
tb.Button(app, text="📃 List All Movies", command=list_movies_gui, bootstyle="info", width=30).pack(pady=5)
tb.Button(app, text="❌ Delete Movie", command=delete_movie_gui, bootstyle="danger", width=30).pack(pady=5)
tb.Button(app, text="🚪 Exit", command=app.destroy, bootstyle="secondary", width=30).pack(pady=10)

# Run GUI
app.mainloop()
