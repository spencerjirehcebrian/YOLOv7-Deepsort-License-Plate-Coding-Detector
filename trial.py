import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Number Selection")

# Create a label
label = tk.Label(root, text="Select a number:")
label.pack()

# Create a variable to store the selected number
selected_number = tk.StringVar()

# Create a dropdown menu with numbers
number_choices = [str(i) for i in range(1, 11)]
number_dropdown = ttk.Combobox(root, textvariable=selected_number, values=number_choices)
number_dropdown.pack()

# Function to handle the selection
def on_select(event):
    selected_value = selected_number.get()
    label.config(text=f"Selected number: {selected_value}")

number_dropdown.bind("<<ComboboxSelected>>", on_select)

# Start the tkinter main loop
root.mainloop()
