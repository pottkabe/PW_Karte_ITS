import tkinter as tk
from pymongo import MongoClient
from tkinter import filedialog
from tkinter import *

# Verbindung zur Datenbank aufbauen
client = MongoClient()
db = client.woerterbuch
collection = db.woerter

def oeffne_datei():
    pwListe=filedialog.askopenfile(initialdir="E:/Studium/Python Code", filetypes=[(('Text Dateien', '*.txt'))]).readlines()
    for wort in pwListe:
        eintrag=collection.find_one({'_id':wort.strip()})
        if eintrag:
            listbox.insert(tk.END, wort)
        else:
            listbox2.insert(tk.END, wort)

def reset_listen():
    listbox.delete(0,END)
    listbox2.delete(0, END)
    trace([0,0,(0,),((0,0),)])
    eingabe.delete(0,END)

# Markierung der Teilabschnitte

def gehe_horizontal(spalte, zeile, schritte, richtung=1):
    for i in range(0, schritte):
        karte_2d[zeile][spalte].config(bg='blue')
        spalte += richtung
    return (spalte - richtung, zeile)

def gehe_vertikal(spalte, zeile, schritte, richtung=1):
    for i in range(0, schritte):
        karte_2d[zeile][spalte].config(bg='blue')
        zeile += richtung
    return (spalte, zeile - richtung)


def gehe_diagonal(spalte, zeile, schritte, richtung_X, richtung_Y):
    for i in range(0, schritte):
        karte_2d[zeile][spalte].config(bg='blue')
        spalte += richtung_X
        zeile += richtung_Y
    return (spalte - richtung_X, zeile - richtung_Y)

# Hauptfunktion zur Markierung des Wortes auf der Karte

def trace(weg):
    spalte=weg[0]
    zeile=weg[1]
    teilwege=weg[2]
    richtungs_permutation=weg[3]
    for a in karte_2d:
        for b in a:
            b.config(bg='#aaeaff')
    for i in range(len(teilwege)):
        if richtungs_permutation[i][0] and not richtungs_permutation[i][1]:
            wort_tpl = gehe_horizontal(spalte, zeile, teilwege[i], richtungs_permutation[i][0])
        if not richtungs_permutation[i][0] and richtungs_permutation[i][1]:
            wort_tpl = gehe_vertikal(spalte, zeile, teilwege[i], richtungs_permutation[i][1])
        if richtungs_permutation[i][0] and richtungs_permutation[i][1]:
            wort_tpl = gehe_diagonal(spalte, zeile, teilwege[i], richtungs_permutation[i][0],
                                     richtungs_permutation[i][1])
        if i < len(teilwege) - 1:
            spalte = wort_tpl[0] + richtungs_permutation[i + 1][0]
            zeile = wort_tpl[1] + richtungs_permutation[i + 1][1]

# Suche nach einem Wort n der Datenbank

def suche_nach_eintrag():
    ampel_gruen.config(bg='white')
    ampel_rot.config(bg='white')
    wort=eingabe.get()
    eintrag=collection.find_one({'_id':wort})
    if eintrag:
        ampel_gruen.config(bg="green")
        print(wort, eintrag['path'])
        # Wenn das  Wort gefunden wurde, markiere es auf der Karte
        trace(eintrag['path'])
        listbox.insert(tk.END, wort)
    else:
        ampel_rot.config(bg="red")
        listbox2.insert(tk.END, wort)

# Zeige ein Passwort aus der Gefunden Liste auf der Kartet

def zeige_weg():
    if listbox.curselection():
        index = listbox.curselection()[0]
        pw_aus_liste=listbox.get(index).strip()
        eintrag = collection.find_one({'_id':pw_aus_liste})
        trace(eintrag['path'])

# GUI

window = tk.Tk()
window.title('Passwortkarte GUI')

# Frame unterhalb der Karte


# Frame der die Kare und die History enthält
top_frame = tk.Frame(window)
top_frame.grid()

bottom_frame = tk.Frame(window)
bottom_frame.grid(sticky='W')
# Frame mit der Karte
karten_frame = tk.Frame(top_frame)
karten_frame.grid(column=0,row=0)

# Frames die die Listenn gefundener und nicht gefundener Passwrter enthält
history_frame1 = tk.Frame(top_frame)
history_frame1.grid(column=1,row=0,sticky='N')

history_frame2 = tk.Frame(top_frame)
history_frame2.grid(column=2,row=0,sticky='N')

karte_2d=[]
karte =['Uk8Wg2Uq2Mu13p9Sd1Fz9Yr6Hg', '2h66#Q4sB7#D9CS2$45gT9#tX1', 'aWy3tCp1u7y6kEg4nBq6mDg7rV', '$1O@2Y&8P§1E&6O&95§8K$6Q$1',
       '§&I4#Hfy65&a9AGdo#O@oQI&1#', 'Oa11b3ZI2Ky9Sm6Po14i4Bk8Fa', '7kV2%E3nO5&O3rA7@W5vG3@y31', 'iMo3qDq1pOp1yUq6u1b6nDh7xO',
       '§1T$1X@27#5F@1Y#2L§1X$69§6', '%§X5%HpcA7e5S5wy$7@gRbp#3#', 'Pd7Re9HI12e7Kq7Mj8Ew4Yt25e', '2oI6$V3jS2%I2o53&T9hP6&tH1']

# Erstellt die Karte
for i in range(len(karte)):
    karte_2d.append([])
    for j in range(len(karte[i])):
        karte_2d[i].append(tk.Label(karten_frame, text=karte[i][j], bg="#aaeaff",width=3, font=("Arial Bold", 16)))
        karte_2d[i][j].grid(column=j, row=i)

# Suchen Button mit dem die SUche nach dem eingegebene Wort startet
finde=tk.Button(bottom_frame, text='Suchen', font=("Arial Bold", 14), command=suche_nach_eintrag)
finde.grid(column=0,row=0,sticky='W', padx=5, pady=5)
# PW Eingabe Feld in dem das zu suchende Wort eingegeben wird
eingabe=tk.Entry(bottom_frame, width=30, font=("Arial", 14))
eingabe.grid(column=1, row=0,padx=5, pady=5)
eingabe.bind('<Return>', lambda x: finde.invoke())
# Ampel, die anzegt, ob ein Wort gefunden wurde oder nicht
ampel_rot=tk.Label(bottom_frame, width=5)
ampel_gruen=tk.Label(bottom_frame, width=5)
ampel_rot.grid(column=3, row=0)
ampel_gruen.grid(column=4, padx=5, row=0)
# Bulk Datei einlesen Button
lade_Bulk_Datei = tk.Button(bottom_frame, text="Lade Bulk Datei", font=("Arial Bold", 14), command=oeffne_datei)
lade_Bulk_Datei.grid(column=5, row=0, padx=5, sticky="E")
# Anzeigen Button, mit dem man ein PW aus der Gefunden Liste auf der Karte anzeigen lassen kann
anzeigen = tk.Button(bottom_frame, text="Anzeigen", font=("Arial Bold", 14), command=zeige_weg)
anzeigen.grid(column=6, row=0, padx=5, sticky="E")
# Reset Button, Setzt alle Felder auf Anfangszustand zurück
reset = tk.Button(bottom_frame, text="Reset", font=("Arial Bold", 14), command=reset_listen)
reset.grid(column=7, row=0, padx=5, sticky="E")
# Liste mit den gefundenen Passwoertern
gefunden=tk.Label(history_frame1, text="Gefunden", font=("Arial Bold", 16))
gefunden.pack()
Scroll_text=Scrollbar(history_frame1)
Scroll_text.pack(side=RIGHT, fill=Y)
listbox = Listbox(history_frame1, yscrollcommand=Scroll_text.set,height=20, selectmode=SINGLE)
Scroll_text.config(command=listbox.yview)
listbox.pack(side=LEFT, fill=BOTH)
listbox.bind('<Double-1>', lambda x: anzeigen.invoke())
# Liste mit den Nicht gefundenen Passwoertern
nicht_gefunden=tk.Label(history_frame2, text="Unbekannt", font=("Arial Bold", 16))
nicht_gefunden.pack()
Scroll_text2=Scrollbar(history_frame2)
Scroll_text2.pack(side=RIGHT, fill=Y)
listbox2 = Listbox(history_frame2, yscrollcommand=Scroll_text2.set,height=20, selectmode=SINGLE)
Scroll_text2.config(command=listbox2.yview)
listbox2.pack(side=LEFT, fill=BOTH)

window.mainloop()