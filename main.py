import requests
from bs4 import BeautifulSoup

page_to_parse = requests.get("https://www.radiokawa.com/episode/late-late-boudoir-gambetta/")

'''
Les podcasts à dl :
e-dixit : https://www.radiokawa.com/episode/e-dixit-1/
Comics outcast : https://www.radiokawa.com/culture-et-arts/comics-outcast/
Morceaux choisis : https://www.radiokawa.com/musique/morceaux-choisis/
Faster Than Light : https://www.radiokawa.com/jeux-video/faster-than-light/
Les démons du Midi : https://www.radiokawa.com/jeux-video/les-demons-du-midi/
'''

# TODO : Vérifier que la sortie pour les différents podcasts. Faire une branche par podcast ?

parsed_page = BeautifulSoup(page_to_parse.text, features="html.parser")

# print(parsed_page)

mp3_link_list = parsed_page.find_all("a", {"class": "download-button"})
mp3_link_list = mp3_link_list[1:]

for i in range(len(mp3_link_list)):
    print(mp3_link_list[i]['href'])

episode_link = parsed_page.find_all("a", {"class": "episode-link"})

for i in range(len(episode_link)):
    page_to_parse = requests.get(episode_link[i]['href'])
    parsed_page = BeautifulSoup(page_to_parse.text, features="html.parser")
    my_div = parsed_page.find_all("div", {"class": "episode-description"})
    episode_title = parsed_page.find("h1", {"class": "episode-title"}).contents
    episode_subtitle = parsed_page.find("div", {"class": "episode-subtitle"}).contents
    episode_date = parsed_page.find("div", {"class": "episode-date"}).contents
    episode_desc = parsed_page.find("div", {"class": "episode-content text-copy"}).contents
    episode_thumbnail = str(parsed_page.find("div", {"class": "episode-thumbnail"})['style']).split('(')[1][:-2]
    #print("Titre : "+str(episode_title[0])+"\nSous-titre : "+str(episode_subtitle[0])+"\nDate : "+str(episode_date)+"\nDescription : "+str(episode_desc)+"\n\n")
    print(episode_thumbnail)


'''
for i in range(len(button_link)):
    print(button_link[i]) #['href'])
'''

'''
episode_to_get = mp3_link_list[1]['href']
episode = requests.get(episode_to_get)

with open('./episode.mp3', 'wb') as f:
    f.write(episode.content)

print(episode.status_code)
print(episode.headers['content-type'])
print(episode.encoding)
'''

