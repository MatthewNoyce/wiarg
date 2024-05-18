#https://www.youtube.com/watch?v=5qOnzF7RsNA
#inspired by this video 
import tkinter as tk
from PIL import ImageTk
import sqlite3
from numpy import random 
import pyglet

bg_colour = "#3d6466"

# pyglet.font.add_file(r"C:\Users\matth\Documents\wiarg\starter_files\fonts\Ubuntu-Bold.ttf")
# pyglet.font.add_file(r"C:\Users\matth\Documents\wiarg\starter_files\fonts\Shanti-Regular.ttf")

def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def fetch_db():
    connection = sqlite3.connect("starter_files/data/recipes.db")
    cursor  = connection.cursor()
    #should save table names in csv file and access that instead
    cursor.execute("SELECT * FROM sqlite_schema WHERE type='table';")
    all_tables = cursor.fetchall()
    #random recipe
    idx = random.randint(0, len(all_tables)-1)

    #access ingredients
    table_name = all_tables[idx][1]
    cursor.execute("SELECT * FROM " + table_name + ";")
    table_records = cursor.fetchall()

    connection.close()
    return table_name, table_records

def pre_process(table_name, table_records):
    #title
    title = table_name[:-6]
    title = "".join([char if char.islower() else " " + char for char in title])
    
    ingredients = []
    #ingredients
    for i in table_records:
        name = i[1]
        qty = i[2]
        unit = i[3]
        ingredients.append(qty + " " + unit + " of " + name)

    return title, ingredients

def load_frame1():
    clear_widgets(frame2)
    frame1.tkraise()
    #stopes background from changing colour
    frame1.pack_propagate(False)
    #logo widget
    logo_img = ImageTk.PhotoImage(file="starter_files/assets/wiarg.png")
    logo_widget = tk.Label(frame1, image=logo_img, bg=bg_colour)
    logo_widget.image = logo_img
    logo_widget.pack()
    #title
    tk.Label(frame1, text="Recipe", bg=bg_colour, fg="white", font=("TkMenuFont", 14)).pack(pady=20)
    #button widget
    tk.Button(frame1, text="shuffle", font=("TkHeadingFont", 20), bg="#28393a", fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black", command=lambda:load_frame2()).pack(pady=20)


def load_frame2():
    clear_widgets(frame1)
    table_name, table_records = fetch_db()
    title, ingredients = pre_process(table_name, table_records)
    frame2.tkraise()
    #logo widget
    logo_img = ImageTk.PhotoImage(file="starter_files/assets/wiarg.png")
    logo_widget = tk.Label(frame2, image=logo_img, bg=bg_colour)
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)
    #title
    tk.Label(frame2, text=title, bg=bg_colour, fg="white", font=("TkHeadingFont", 20)).pack(pady=25)
    #ingredients list
    for i in ingredients:
        tk.Label(frame2, text=i, bg="#28393a", fg="white", font=("TkMenuFont", 12)).pack(fill="both")
    #back button
    tk.Button(frame2, text="back", font=("TkHeadingFont", 18), bg="#28393a", fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black", command=lambda:load_frame1()).pack(pady=20)

    


#revised logic for centering
# x = root.winfo_screenwidth() //2
# y = int(root.winfo_screenheight()*0.1)
# #geometry 500x600 width+heinght, x=position y=position
# root.geometry ("500x600+" + str(x) + "+" + str(y))
root = tk.Tk()
root.title("Recipe Picker")

root.eval("tk::PlaceWindow . center")

frame1 = tk.Frame(root, width=500, height=600, bg=bg_colour)
frame2 = tk.Frame(root, bg=bg_colour)

for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="nesw")

load_frame1()

#widgets

# run app

root.mainloop()