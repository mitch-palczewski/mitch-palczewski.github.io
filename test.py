#!/usr/bin/env python3
import tkinter as tk

# Adjust this import to point at where your ScrollText class lives
from app.gui.widgets.text import ScrollText
# Ensure BaseStyle is on the import path
from app.gui.styles import BaseStyle

def main():
    root = tk.Tk()
    root.title("ScrollText Test")

    # Instantiate ScrollText (uses BaseStyle internally)
    scroll = ScrollText(root, width=60, height=15)
    scroll.pack(padx=10, pady=10, fill="both", expand=True)

    # Insert sample text
    sample_text = "\n".join(f"Line {i}" for i in range(1, 21))
    scroll.insert("1.0", sample_text)

    # Button to print current contents to console
    def on_print():
        print("=== ScrollText Contents ===")
        print(scroll.get_all())

    btn = tk.Button(root, text="Print Contents", command=on_print)
    btn.pack(pady=(0,10))

    root.mainloop()

if __name__ == "__main__":
    main()