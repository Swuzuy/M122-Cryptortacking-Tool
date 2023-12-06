import tkinter as tk

# Erstelle das Hauptfenster
root = tk.Tk()

# Funktion zur Anpassung der Größe des Fensters
def resize_window():
    root.geometry("400x300")  # Ändere die Größe des Fensters auf 400x300

# Button zur Größenanpassung
resize_button = tk.Button(root, text="Größe anpassen", command=resize_window)
resize_button.pack()  # Zeige den Button im Fenster an

# Starte die UI-Schleife
root.mainloop()
