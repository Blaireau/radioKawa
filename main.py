import requests
from bs4 import BeautifulSoup

page_to_parse = requests.get("https://www.radiokawa.com/episode/late-late-boudoir-gambetta-1/")
# page_to_parse = requests.get("https://www.radiokawa.com/culture-et-arts/comics-outcast/")
# page_to_parse = requests.get("https://www.radiokawa.com/musique/morceaux-choisis/")
parsed_page = BeautifulSoup(page_to_parse.text, features="html.parser")

button_link = parsed_page.find_all("a", {"class": "download-button"})
button_link = button_link[1:]

for i in range(len(button_link)):
    print(button_link[i]['href'])

episode_to_get = button_link[1]['href']
episode = requests.get(episode_to_get)

with open('./episode.mp3','wb') as f:
    f.write(episode.content)

print(episode.status_code)
print(episode.headers['content-type'])
print(episode.encoding)