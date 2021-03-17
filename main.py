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
import libs/download_lib


# Defining the different events
def updateShowList(event):
    # Obtenir l'élément sélectionné
    selectedShow = listeCatCombo.get()
    print("Vous avez sélectionné : '", selectedShow, "'")
    listeShow = getShowList(baseUrl, selectedShow.replace(" ","-"))


def updateEpisodeList(event):
    print(event)


# Variables
listeCat = ["le vrac", "culture et arts", "jeux video", "musique", "technologie", "la vie", "les archives"]
listeShow = [""]
baseUrl = "https://www.radiokawa.com/"

# Building the GUI
mainWindow = tk.Tk()
mainWindow.geometry('300x200')
# Windows Title
mainWindow.title("Radio Kawa Dowloader")
# Small 
labelChoix = tk.Label(mainWindow, text="Radio Kawa Downloader ! \n Assurez vous que le site soit toujours up !")
labelChoix.pack()

# Adding the category list
labelDescCat = tk.Label(mainWindow, text="Quelle catégorie souhaitez vous ?")
labelDescCat.pack()

# Create the Combobox, set the first element by default, pack and bind an action
listeCatCombo = ttk.Combobox(mainWindow, values=listeCat)
listeCatCombo.current(0)
listeCatCombo.pack()
listeCatCombo.bind("<<ComboboxSelected>>", updateShowList)

labelDescShow = tk.Label(mainWindow, text="Quelle émission souhaitez vous ?")
labelDescShow.pack()

listeShowCombo = ttk.Combobox(mainWindow, values=listeShow)
listeShowCombo.current(0)
listeShowCombo.pack()
listeShowCombo.bind("<<ComboboxSelected>>", updateEpisodeList)

mainWindow.mainloop()
