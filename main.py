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
import os
from libs import gen_epub

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
        infoBar['text'] = 'Téléchargement de l\'épisode : '+ str(count) +'/'+ str(len(episodeDict))
        getEpisode(categorie, show, episodeDict[i])
        count += 1
        mainWindow.update_idletasks()
        time.sleep(1)
    infoBar['text'] = 'Tous les épisodes sont téléchargés !'


# Download one episode within the correct path.
def getEpisode(categorie, show, episodeUrl):
    illegalChar = '<>\/:*?"|'
    full_path = "./download/"+ categorie.replace(" ","_") + "/" + show.replace(" ","_")
    # Check if the directory exists and create it
    os.makedirs(full_path, exist_ok=True)
    # Getting the page
    pageToDl = requests.get(episodeUrl)
    pageToDlParsed = BeautifulSoup(pageToDl.text, features="html.parser")
    episodeTitle = pageToDlParsed.find("h1", {"class": "episode-title"}).contents
    episodeSubTitle = pageToDlParsed.find("div", {"class": "episode-subtitle"}).contents
    episodeMp3Link = pageToDlParsed.find("a", {"class": "button download-button radstats-download"})['href']
    full_title = str(episodeTitle[0]+" - "+episodeSubTitle[0]).replace(" ", "_")
    for iChar in illegalChar:
        full_title = full_title.replace(iChar, '')
    full_path = full_path + '/' + full_title + '.mp3'
    # Download only if file doesn't exist !
    if os.path.exists(full_path):
        infoBar['text'] = 'Episode déjà téléchargé !'
    else:
        progress['value'] = 0
        with open(full_path, 'wb') as f:
            episode = requests.get(episodeMp3Link, stream=True)
            total_length = episode.headers.get('content-length')
            if total_length is None:
                print("No content-length header...")
                f.write(episode.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in episode.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    progress['value'] = ((100 * dl) / total_length)
                    print((str((100 * dl) / total_length)))
                    mainWindow.update()
        f.close()
    infoBar['text'] = 'Téléchargement fini !'


# Variables
listeCat = ["le vrac", "culture et arts", "jeux video", "musique", "technologie", "la vie", "tv cinema", "les archives"]
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

progress = ttk.Progressbar(mainWindow, length=250, mode='determinate', maximum=100)
progress.pack(pady=10)

infoBar = tk.Label(mainWindow, text="")
infoBar.pack()

mainWindow.mainloop()
