import requests
from bs4 import BeautifulSoup

# Download an episode within the correct path.
def download_episode(url, path, name):
    full_path = path + '/' + podcast_name + '/' + name + '_-_'

    with open(full_path + '.mp3', 'wb') as f:
        episode = requests.get(url, stream=True)
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
                done = int(50 * dl / total_length)
                os.sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                os.sys.stdout.flush()
    f.close()


def get_image(url):
    image = requests.get(url)
    return image.content


# Get the podcast page.
page_to_parse = requests.get("")
# Change for every podcast
podcast_name = ""
parsed_page = BeautifulSoup(page_to_parse.text, features="html.parser")

# Get all link for mp3 download
mp3_link_list = parsed_page.find_all("a", {"class": "download-button"})
mp3_link_list = mp3_link_list[1:]
mp3_link_list.reverse()

# Get all page link for every episode
# Needed to build the output document
episode_link = parsed_page.find_all("a", {"class": "episode-link"})
episode_link.reverse()

# Create the output document
output_doc = OpenDocumentText()
my_styles = output_doc.styles
my_styles.addElement(pStyle)
my_styles.addElement(subtitleStyle)
my_styles.addElement(titleStyle)
my_styles.addElement(p_with_break)
my_styles.addElement(dateStyle)

for i in range(len(episode_link)):
    page_to_parse = requests.get(episode_link[i]['href'])
    parsed_page = BeautifulSoup(page_to_parse.text, features="html.parser")
    my_div = parsed_page.find_all("div", {"class": "episode-description"})
    episode_title = parsed_page.find("h1", {"class": "episode-title"}).contents
    episode_subtitle = parsed_page.find("div", {"class": "episode-subtitle"}).contents
    episode_date = parsed_page.find("div", {"class": "episode-date"}).contents
    episode_date = format_date(episode_date)
    episode_desc = parsed_page.find("div", {"class": "episode-content text-copy"}).contents
    episode_desc = format_desc(episode_desc)
    episode_voices = parsed_page.find("div", {"class": "episode-voices"}).contents
    episode_voices = format_voices(episode_voices)
    episode_thumbnail = str(parsed_page.find("div", {"class": "episode-thumbnail"})['style']).split('(')[1][:-2]
    try:
        extra_content = parsed_page.find("div", {"class": "extra-content text-copy"}).contents
        print(extra_content[0].find("a")['href'])
    except AttributeError:
        print("No Extra content")
        print(extra_content)
        #extra_content = 'None'
    except TypeError:
        print(type(extra_content))
        print(extra_content)

    print("Titre : " + str(episode_title[0]) + "\nSous-titre : " + str(episode_subtitle[0]) + "\nDate : " + str(
        episode_date) + "\nDescription : " + str(episode_desc) + "\nAnimateurs : " + str(episode_voices) +
        "\nExtra Content : " + str(extra_content))
    print("Téléchargement de l'épisode en cours...")
    # download_episode(mp3_link_list[i]['href'], '.', str(episode_title[0]).replace(' ', '_'))
    print("\nTéléchargement fini")

    print("Mise à jour du fichier doc")
    document_generation(output_doc, episode_title, episode_subtitle, episode_date, episode_desc, episode_voices,
                        episode_thumbnail)
    print("Mise à jour finie. Episode suivant !\n")
