'''
Les podcasts à dl :
e-dixit : https://www.radiokawa.com/episode/e-dixit-1/
Comics outcast : https://www.radiokawa.com/culture-et-arts/comics-outcast/
Morceaux choisis : https://www.radiokawa.com/musique/morceaux-choisis/
Faster Than Light : https://www.radiokawa.com/jeux-video/faster-than-light/
Les démons du Midi : https://www.radiokawa.com/jeux-video/les-demons-du-midi/
La Dev Team : https://www.radiokawa.com/jeux-video/la-dev-team/
Les game makers : https://www.radiokawa.com/jeux-video/the-game-makers/
Ludographie comparée : https://www.radiokawa.com/episode/ludographie-comparee-61/
Kaorin : https://www.radiokawa.com/episode/kaorin-134/
'''

# Imports
import tkinter as tk
from tkinter import ttk
#import libs/gen_epub
#import libs/download_lib

root = tk.Tk()
root.geometry('300x200')


def action(event):
    # Obtenir l'élément sélectionné
    select = listeCombo.get()
    tmp = "Vous avez sélectionné : " + select
    labelOut['text'] = tmp
    print("Vous avez sélectionné : '", select, "'")


labelChoix = tk.Label(root, text="Veuillez faire un choix !")
labelChoix.pack()

labelOut = tk.Label(root, text="Vous avez sélectionné : ")
labelOut.pack()

# 2) - créer la liste Python contenant les éléments de la liste Combobox
listeProduits = ["Laptop", "Imprimante", "Tablette", "SmartPhone"]

# 3) - Création de la Combobox via la méthode ttk.Combobox()
listeCombo = ttk.Combobox(root, values=listeProduits)

# 4) - Choisir l'élément qui s'affiche par défaut
listeCombo.current(0)

listeCombo.pack()
listeCombo.bind("<<ComboboxSelected>>", action)

root.mainloop()
