import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cryptocompare
from datetime import datetime, timedelta

class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Price Viewer")
        self.root.geometry("800x600")
        self.root.configure(bg="white")  # Hintergrundfarbe des Hauptfensters

        # Frame für den Seitenbalken
        sidebar_frame = tk.Frame(root, bg="#1f1f1f")  # Dunkler Hintergrund für den Seitenbalken
        sidebar_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons im Seitenbalken als Ovale mit dunklerem Stil
        buttons = ["Bitcoin", "Ethereum", "Cardano", "Tag", "Monate", "Jahr"]
        for button_text in buttons:
            button = tk.Button(sidebar_frame, text=button_text, command=lambda bt=button_text: self.handle_button_click(bt),
                                relief=tk.GROOVE, borderwidth=3, width=15, height=2, bg="#333333", fg="white")
            button.pack(fill=tk.X, pady=10)

        # Frame für den Graph und den Preis mit weißem Hintergrund
        content_frame = tk.Frame(root, bg="white")  # Hintergrundfarbe für den Graphen
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Initialisierung des Graphs
        self.fig, self.ax = plt.subplots(figsize=(6, 4), dpi=100)
        self.ax.set_facecolor('white')  # Hintergrundfarbe des Graphen
        self.canvas = FigureCanvasTkAgg(self.fig, master=content_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Label für den aktuellen Preis mit weißem Hintergrund
        self.price_label = tk.Label(content_frame, text="", font=("Helvetica", 14), bg="white", fg="#1f1f1f")
        self.price_label.pack(side=tk.BOTTOM, pady=10)

        # Initialisierung der Timer-ID für die Preisaktualisierung
        self.update_timer_id = None
        # Initialisierung der Standard-Zeitspanne
        self.time_range = "Tag"
        # Aktualisiere den Graph und den Preis beim Start
        self.show_chart("Bitcoin")

    def handle_button_click(self, button_text):
        if button_text in ["Tag", "Monate", "Jahr"]:
            self.time_range = button_text
            # Aktualisiere den Graph mit der neuen Zeitspanne
            self.show_chart("Bitcoin")
        else:
            # Handhabung für die Cryptocurrency-Buttons
            self.show_chart(button_text)

    def show_chart(self, coin):
        try:
            # Lade historische Daten für den ausgewählten Coin und die entsprechende Zeitspanne
            coin_symbol = self.get_coin_symbol(coin)
            data = self.get_historical_data(coin_symbol, self.time_range)

            if data is None or not data:  # Überprüfe, ob Daten vorhanden sind
                raise ValueError("Keine Daten verfügbar.")

            # Extrahiere Daten für den Plot
            dates = [datetime.utcfromtimestamp(entry['time']).strftime('%Y-%m-%d') for entry in data]
            prices = [entry['close'] for entry in data]

            # Bestimme die Farbe basierend auf Kursänderungen
            colors = ['green' if prices[i] < prices[i + 1] else 'red' for i in range(len(prices) - 1)]
            colors.append(colors[-1])  # Wiederhole die letzte Farbe für den letzten Punkt

            # Aktualisiere den Plot
            self.ax.clear()
            for i in range(len(dates) - 1):
                self.ax.plot([dates[i], dates[i + 1]], [prices[i], prices[i + 1]], color=colors[i], marker='o', markersize=5, markerfacecolor='black', markeredgecolor='black')

            self.ax.legend([coin], loc='upper left')
            self.ax.set_xticklabels(dates, rotation=45, ha='right')  # Drehung der Datumsangaben
            self.ax.set_facecolor('white')  # Hintergrundfarbe des Graphen

            # Füge vertikale und horizontale Linien für jeden Tag hinzu
            for date in dates:
                self.ax.axvline(x=date, color='#1f1f1f', linestyle='--', linewidth=0.5)  # Dunklere vertikale Linie
                self.ax.axhline(y=max(prices), color='red', linestyle='--', linewidth=0.5)  # Beispiel für horizontale Linie

            self.canvas.draw()

            # Zeige den aktuellen Preis an
            current_price = cryptocompare.get_price(coin_symbol, currency="USD")[coin_symbol]["USD"]
            self.price_label.config(text=f"Aktueller Preis von {coin}: ${current_price:.2f}")

            # Starte die kontinuierliche Aktualisierung des Preises
            self.start_price_update(coin)
        except Exception as e:
            print(f"Fehler beim Laden der Daten für {coin}: {e}")
            self.price_label.config(text=f"Fehler beim Laden der Daten für {coin}")

    def get_historical_data(self, coin_symbol, time_range):
        # Bestimme das Startdatum basierend auf der ausgewählten Zeitspanne
        if time_range == "Tag":
            start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        elif time_range == "Monate":
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        elif time_range == "Jahr":
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        else:
            raise ValueError("Ungültige Zeitspanne")

        # Lade historische Daten für den ausgewählten Coin und die entsprechende Zeitspanne
        data = cryptocompare.get_historical_price_day(coin_symbol, currency="USD", limit=30, toTs=start_date)
        return data

    def get_coin_symbol(self, coin):
        # Mapping von Coin-Namen zu Coin-Symbolen
        coin_mapping = {
            "Bitcoin": "BTC",
            "Ethereum": "ETH",
            "Cardano": "ADA",
            # Weitere Mappings hinzufügen, falls erforderlich
        }
        return coin_mapping.get(coin, coin)

    def start_price_update(self, coin):
        # Setze die Funktion für die kontinuierliche Aktualisierung im Zeitintervall
        self.update_timer_id = self.root.after(60000, lambda: self.update_price(coin))

    def update_price(self, coin):
        try:
            coin_symbol = self.get_coin_symbol(coin)
            current_price = cryptocompare.get_price(coin_symbol, currency="USD")[coin_symbol]["USD"]
            self.price_label.config(text=f"Aktueller Preis von {coin}: ${current_price:.2f}")

            # Setze die Funktion für die kontinuierliche Aktualisierung im Zeitintervall
            self.update_timer_id = self.root.after(60000, lambda: self.update_price(coin))
        except Exception as e:
            print(f"Fehler beim Laden der Daten für {coin}: {e}")
            self.price_label.config(text=f"Fehler beim Laden der Daten für {coin}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()