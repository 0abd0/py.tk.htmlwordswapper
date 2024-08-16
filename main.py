import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # For styled widgets


# Function to connect to SQLite database
def connect_to_db():
    connection = sqlite3.connect('example.db')
    return connection


# Function to create the table if it doesn't exist
def create_table():
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS replacements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            original_word TEXT,
            replacement_word TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    connection.commit()
    connection.close()


# Function to browse files
def browse_files():
    file_path = filedialog.askopenfilename(
        filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
    )
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)


# Function to search and replace words in HTML
def search_and_replace():
    file_path = file_path_entry.get()
    search_word = search_word_entry.get()
    replacement_option = replacement_option_entry.get()
    connection = connect_to_db()

    if file_path and search_word and connection:
        try:
            with open(file_path, "r") as file:
                content = file.read()

            replacement_counter = 1
            results = []

            while search_word in content:
                if replacement_option:
                    new_word = replacement_option
                else:
                    new_word = str(replacement_counter)
                content = content.replace(search_word, new_word, 1)
                results.append(f"Replaced '{search_word}' with '{new_word}'")
                replacement_counter += 1

            with open(file_path, "w") as file:
                file.write(content)

            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO replacements (file_name, original_word, replacement_word) VALUES (?, ?, ?)",
                (file_path, search_word, replacement_option if replacement_option else "1, 2, 3, ...")
            )
            connection.commit()

            messagebox.showinfo("Replacement Results", "\n".join(results))

        except Exception as e:
            result_label.config(text=f"Error: {e}")
        finally:
            connection.close()
    else:
        result_label.config(text="Please select a file and enter a word to search.")


# Main Tkinter window
root = tk.Tk()
root.title("HTML Word Replacer")

# Set window size
root.geometry("600x600")

# Set background image
background_image = tk.PhotoImage(file="C:/Users/abd.shehada/Downloads/2.png")
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)
tk.Label(text="0abd0").grid(row=0, column=0, padx=10, pady=10)

# Frame to hold the widgets (to place them over the background)
frame = tk.Frame(root, bg='#ffffff', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.5, anchor='n')

# File path entry
tk.Label(frame, text="HTML File:").grid(row=0, column=0, padx=10, pady=10)
file_path_entry = tk.Entry(frame, width=50)
file_path_entry.grid(row=0, column=1, padx=10, pady=10)
browse_button = tk.Button(frame, text="Browse", command=browse_files)
browse_button.grid(row=0, column=2, padx=10, pady=10)

# Search word entry
tk.Label(frame, text="Word to search:").grid(row=1, column=0, padx=10, pady=10)
search_word_entry = tk.Entry(frame, width=50)
search_word_entry.grid(row=1, column=1, padx=10, pady=10)

# Replacement option entry
tk.Label(frame, text="Replace with (leave blank for numbering):").grid(row=2, column=0, padx=10, pady=10)
replacement_option_entry = tk.Entry(frame, width=50)
replacement_option_entry.grid(row=2, column=1, padx=10, pady=10)

# Replace button
replace_button = tk.Button(frame, text="Search and Replace", command=search_and_replace)
replace_button.grid(row=3, column=1, padx=10, pady=10)

# Result label
result_label = tk.Label(frame, text="", bg='#ffffff')
result_label.grid(row=4, column=1, padx=10, pady=10)

# Call the create_table function to ensure the database table exists
create_table()

# Start the Tkinter event loop
root.mainloop()
