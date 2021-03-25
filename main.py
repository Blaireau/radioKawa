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
# import libs/gen_epub
from libs import download_lib

listeShowDict = {}
listeEpisodeDict = {}


# Defining the different events
def updateShowList(event):
    global listeShowDict
    # Obtenir l'élément sélectionné
    selectedShow = listeCatCombo.get()
    listeShowDict = download_lib.getShowList(baseUrl, selectedShow.replace(" ", "-"))
    listeShowCombo['values'] = list(listeShowDict.keys())


def updateEpisodeList(event):
    global listeEpisodeDict
    print(listeShowDict[listeShowCombo.get()])
    listeEpisodeDict = download_lib.getEpisodeList(listeShowDict[listeShowCombo.get()], listeCatCombo.get())
    listeEpisodeCombo['values'] = list(listeEpisodeDict.keys())


def downloadEpisode():
    if listeEpisodeCombo.get() == 'all':
        download_lib.downloadAllEpisode(listeCatCombo.get(), listeShowCombo.get(), listeEpisodeDict)
    else:
        download_lib.downloadEpisode(listeCatCombo.get(), listeShowCombo.get(), listeEpisodeDict[listeEpisodeCombo.get()])
#        print(listeCatCombo.get())
#        print(listeShowCombo.get())
#        print(str(listeEpisodeCombo.get()) + " : " + str(listeEpisodeDict[listeEpisodeCombo.get()]))
#        print(buttonStatus.get())


# Variables
listeCat = ["le vrac", "culture et arts", "jeux video", "musique", "technologie", "la vie", "les archives"]
listeShow = [""]
listeEpisode = [""]
baseUrl = "https://www.radiokawa.com/"

# Building the GUI
mainWindow = tk.Tk()
mainWindow.geometry('300x225')
buttonStatus = tk.IntVar()
# Windows Title
mainWindow.title("Radio Kawa Downloader")
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

labelDescShow = tk.Label(mainWindow, text="Quelle numéro souhaitez vous ?")
labelDescShow.pack()

listeEpisodeCombo = ttk.Combobox(mainWindow, values=listeEpisode)
listeEpisodeCombo.current(0)
listeEpisodeCombo.pack()

ePubButton = ttk.Checkbutton(mainWindow, text="Generate epub ?", variable=buttonStatus)
ePubButton.pack()

downloadButton = ttk.Button(mainWindow, text="Download !", command=downloadEpisode)
downloadButton.pack()

mainWindow.mainloop()
