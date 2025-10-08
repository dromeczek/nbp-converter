import requests
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation

def pobierz_kursy():
    """Pobiera aktualne kursy średnie NBP (tabela A)."""
    url = "https://api.nbp.pl/api/exchangerates/tables/A?format=xml"
    resp = requests.get(url)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    kursy = {"PLN": Decimal("1.0")} 
    for rate in root.findall(".//Rate"):
        kod = rate.find("Code").text
        kurs = Decimal(rate.find("Mid").text)
        kursy[kod] = kurs
    return kursy


def przelicz():
    """Wykonuje przeliczenie przez PLN."""
    try:
        kwota = Decimal(entry_kwota.get())
    except InvalidOperation:
        messagebox.showerror("Błąd", "Nieprawidłowa kwota!")
        return

    src = combo_zrodlo.get()
    tgt = combo_cel.get()
    if src not in kursy or tgt not in kursy:
        messagebox.showerror("Błąd", "Wybierz waluty!")
        return

    kurs_src = kursy[src]
    kurs_tgt = kursy[tgt]


    wynik = kwota * (kurs_src / kurs_tgt)

    label_wynik.config(text=f"{kwota} {src} = {wynik.quantize(Decimal('0.01'))} {tgt}")



root = tk.Tk()
root.title("Przelicznik walut NBP")

frame = ttk.Frame(root, padding=15)
frame.grid()

ttk.Label(frame, text="Kwota:").grid(row=0, column=0, sticky="e")
entry_kwota = ttk.Entry(frame, width=15)
entry_kwota.grid(row=0, column=1, padx=5)

ttk.Label(frame, text="Z waluty:").grid(row=1, column=0, sticky="e")
ttk.Label(frame, text="Na walutę:").grid(row=2, column=0, sticky="e")


try:
    kursy = pobierz_kursy()
    kody = sorted(kursy.keys())
except Exception as e:
    messagebox.showerror("Błąd pobierania", str(e))
    kursy = {"PLN": Decimal("1.0")}
    kody = ["PLN"]

combo_zrodlo = ttk.Combobox(frame, values=kody, width=10)
combo_zrodlo.set("USD")
combo_zrodlo.grid(row=1, column=1, padx=5, pady=2)

combo_cel = ttk.Combobox(frame, values=kody, width=10)
combo_cel.set("PLN")
combo_cel.grid(row=2, column=1, padx=5, pady=2)

ttk.Button(frame, text="Przelicz", command=przelicz).grid(
    row=3, column=0, columnspan=2, pady=10
)

label_wynik = ttk.Label(frame, text="", font=("Segoe UI", 12, "bold"))
label_wynik.grid(row=4, column=0, columnspan=2)

root.mainloop()
