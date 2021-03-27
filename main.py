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
import requests
from bs4 import BeautifulSoup
import time
# import libs/gen_epub
# from libs import download_lib

listeShowDict = {}
listeEpisodeDict = {}


# Defining the different events
def updateShowList(event):
    global listeShowDict
    # Obtenir l'élément sélectionné
    selectedShow = listeCatCombo.get()
    listeShowDict = getShowList(baseUrl, selectedShow.replace(" ", "-"))
    listeShowCombo['values'] = list(listeShowDict.keys())


def updateEpisodeList(event):
    global listeEpisodeDict
    print(listeShowDict[listeShowCombo.get()])
    listeEpisodeDict = getEpisodeList(listeShowDict[listeShowCombo.get()], listeCatCombo.get())
    listeEpisodeCombo['values'] = list(listeEpisodeDict.keys())


def downloadEpisode():
    try:
        if listeEpisodeCombo.get() == 'all':
            getAllEpisode(listeCatCombo.get(), listeShowCombo.get(), listeEpisodeDict)
        else:
            getEpisode(listeCatCombo.get(), listeShowCombo.get(), listeEpisodeDict[listeEpisodeCombo.get()])
    except KeyError:
        infoBar['text'] = "Il manque une information !"


def getShowList(baseUrl, catName):
    showDict = {}
    fullUrl = baseUrl + catName
    catPage = requests.get(fullUrl)
    parsedCatPage = BeautifulSoup(catPage.text, features="html.parser")
    catList = parsedCatPage.find_all("div", {"class": "show-title show-title-mobile"})
    for i in catList:
        showDict[i.string] = i.find("a")["href"]
    return showDict


def getEpisodeList(episodesUrl, categorie):
    episodeDict = {"all": "all"}
    episodePage = requests.get(episodesUrl)
    parsedEpisodePage = BeautifulSoup(episodePage.text, features="html.parser")
    episodeNumber = parsedEpisodePage.find_all("div", {"class": "number"})
    episodeName = parsedEpisodePage.find_all("div", {"class": "title"})
    episodeMp3Link = parsedEpisodePage.find_all("a", {"class": "episode-link"})
    if categorie == "les archives":
        episodeName = episodeName[2:]
    else:
        episodeName = episodeName[3:]
    episodeNumber.reverse()
    episodeName.reverse()
    #episodeMp3Link = episodeMp3Link[1:]
    episodeMp3Link.reverse()
    for i in range(len(episodeMp3Link)):
        fullName = episodeNumber[i].text + " - " + episodeName[i].text.strip()
        episodeDict[fullName] = episodeMp3Link[i]['href']
    return episodeDict


def getAllEpisode(categorie, show, episodeDict):
    episodeDict.pop('all')
    count = 1
    for i in episodeDict:
        infoBar['text'] = 'Downloading episode '+ str(count) +'/'+ str(len(episodeDict))
        getEpisode(categorie, show, episodeDict[i])
        count+=1
        mainWindow.update()
        time.sleep(1)


# Download one episode within the correct path.
def getEpisode(categorie, show, episodeUrl):
    full_path = "./"+ categorie.replace(" ","_") + "/" + show.replace(" ","_")
    print(full_path)
    print(episodeUrl)


# Variables
listeCat = ["le vrac", "culture et arts", "jeux video", "musique", "technologie", "la vie", "les archives"]
listeShow = [""]
listeEpisode = [""]
baseUrl = "https://www.radiokawa.com/"

# Building the GUI
mainWindow = tk.Tk()
mainWindow.geometry('300x300')
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

progress = ttk.Progressbar(mainWindow, length = 100, mode = 'determinate')
progress.pack(pady=10)

infoBar = tk.Label(mainWindow, text="")
infoBar.pack()

mainWindow.mainloop()
