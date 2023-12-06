import tkinter as tk

root = tk.Tk()
root.geometry("500x400")

text_label = tk.Label(root, text="Das ist ein Test!")
text_label.pack(pady=50)
text_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

root.mainloop()