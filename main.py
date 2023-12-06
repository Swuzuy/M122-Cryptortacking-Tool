import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta

class CryptoMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Monitor")

        self.crypto_label = ttk.Label(root, text="Kryptowährung:")
        self.crypto_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.crypto_var = tk.StringVar()
        self.crypto_combobox = ttk.Combobox(root, textvariable=self.crypto_var)
        self.crypto_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.crypto_combobox['values'] = ('bitcoin', 'ethereum', 'cardano')
        self.crypto_combobox.current(0)

        self.fetch_button = ttk.Button(root, text="Daten abrufen", command=self.fetch_data)
        self.fetch_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.plot_frame = ttk.Frame(root)
        self.plot_frame.grid(row=1, column=0, columnspan=3)

def fetch_data(self):
    crypto_id = self.crypto_var.get()
    if not crypto_id:
        return

    cg = CoinGeckoAPI()
    crypto_data = cg.get_coin_market_chart_range_by_id(id=crypto_id, vs_currency='usd', from_timestamp=self.get_one_year_ago(), to_timestamp=int(datetime.now().timestamp()))

    print(crypto_data)  # Debug-Ausgabe

    if 'prices' in crypto_data:
        prices = [price[1] for price in crypto_data['prices']]
        timestamps_key = 'timestamps'  # Anpassen, falls der Schlüssel einen anderen Namen hat
        if timestamps_key in crypto_data:
            timestamps = [datetime.fromtimestamp(timestamp/1000) for timestamp in crypto_data[timestamps_key]]
            self.plot_prices(timestamps, prices)

    def get_one_year_ago(self):
        one_year_ago = datetime.now() - timedelta(days=365)
        return int(one_year_ago.timestamp() * 1000)

    def plot_prices(self, timestamps, prices):
        self.plot_frame.destroy()

        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.grid(row=1, column=0, columnspan=3)

        fig, ax = plt.subplots(figsize=(10, 4), tight_layout=True)
        ax.plot(timestamps, prices, marker='o', linestyle='-', color='b')
        ax.set_title('Kursverlauf der Kryptowährung')
        ax.set_xlabel('Datum')
        ax.set_ylabel('Preis in USD')
        ax.xaxis_date()  # Formatiere die x-Achse als Datum

        fig.autofmt_xdate()  # Automatische Anpassung der Datumsetiketten für eine bessere Lesbarkeit

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoMonitorApp(root)
    root.mainloop()

    print("Test")
