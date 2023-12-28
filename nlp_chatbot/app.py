import tkinter as tk
from tkinter import ttk
import random
import sqlite3

# Fungsi untuk mendapatkan respons bot dari database SQLite
def get_bot_response(user_input):
    user_input = user_input.lower()

    conn = sqlite3.connect('bot_responses.db')
    c = conn.cursor()

    # Mencari respons berdasarkan kata kunci
    c.execute("SELECT response FROM bot_responses WHERE keyword LIKE ?", ('%' + user_input + '%',))
    rows = c.fetchall()

    conn.close()

    if rows:
        return random.choice(rows)[0]
    else:
        return random.choice(["Maaf, saya tidak mengerti.", "Tolong tanyakan sesuatu yang lain."])

# Fungsi untuk mengirim pesan
def send_message(event=None):
    user_input = entry_field.get()
    if user_input.strip() != "":
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "You: " + user_input + "\n")
        chat_window.config(state=tk.DISABLED)
        entry_field.delete(0, tk.END)

        bot_response = get_bot_response(user_input)
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "Bot: " + bot_response + "\n")
        chat_window.config(state=tk.DISABLED)
        chat_window.see(tk.END)

# Membuat database dan tabel jika belum ada
conn = sqlite3.connect('bot_responses.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS bot_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT,
                response TEXT
             )''')

# Menambahkan data ke dalam tabel (contoh)
c.execute("INSERT INTO bot_responses (keyword, response) VALUES (?, ?)", ('hai', 'Halo!'))
c.execute("INSERT INTO bot_responses (keyword, response) VALUES (?, ?)", ('hai juga', 'Hai juga!'))
c.execute("INSERT INTO bot_responses (keyword, response) VALUES (?, ?)", ('apa kabar?', 'Baik, terima kasih!'))

conn.commit()
conn.close()

# GUI
root = tk.Tk()
root.title("Chatbox")

style = ttk.Style()
style.theme_use('clam')  # Ganti dengan tema yang diinginkan (misal: 'vista', 'clam', 'alt', dll.)

chat_window = tk.Text(root, bd=1, bg="white", width=50, height=8)
chat_window.config(state=tk.DISABLED)
chat_window.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

entry_field = ttk.Entry(root, width=40)
entry_field.bind("<Return>", send_message)
entry_field.grid(row=1, column=0, padx=5, pady=5)

send_button = ttk.Button(root, text="Send", command=send_message)
send_button.bind("<Button-1>", send_message)
send_button.grid(row=1, column=1, padx=5, pady=5)

root.mainloop()
