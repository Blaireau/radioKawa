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
import requests
from bs4 import BeautifulSoup
from odf.opendocument import OpenDocumentText
from odf.draw import Image, Frame
from odf.style import Style, ParagraphProperties, TextProperties
from odf.text import P
from odf import teletype
import os
import re


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


def format_date(date_to_clean):
    return date_to_clean[0] + ' : ' + re.sub(remove_html, '', str(date_to_clean[1]))


def format_desc(desc_to_clean):
    return 'Description : ' + re.sub(remove_html, '', str(desc_to_clean[0]))


def format_voices(voices_to_clean):
    out_voices = ''
    for j in voices_to_clean[1:]:
        out_voices += re.sub(remove_html, '', str(j))
    return 'Animateur.trice.s : ' + out_voices


# Generate the document
def document_generation(output_doc, episode_title, episode_subtitle, episode_date, episode_desc, episode_voices,
                        episode_thumbnail):
    # Add the title of the episode
    p_element = P(stylename=titleStyle)
    teletype.addTextToElement(p_element, episode_title)
    output_doc.text.addElement(p_element, episode_title)
    teletype.addTextToElement(p_element, line_break)
    output_doc.text.addElement(p_element, line_break)
    # Add the subtitle
    p_element = P(stylename=subtitleStyle)
    teletype.addTextToElement(p_element, episode_subtitle)
    output_doc.text.addElement(p_element, episode_subtitle)
    p_element = P(stylename=dateStyle)
    teletype.addTextToElement(p_element, line_break)
    output_doc.text.addElement(p_element, line_break)
    teletype.addTextToElement(p_element, episode_date)
    output_doc.text.addElement(p_element, episode_date)
    p_element = P(stylename=pStyle)
    teletype.addTextToElement(p_element, line_break)
    output_doc.text.addElement(p_element, line_break)
    teletype.addTextToElement(p_element, episode_desc)
    output_doc.text.addElement(p_element, episode_desc)
    teletype.addTextToElement(p_element, line_break)
    output_doc.text.addElement(p_element, line_break)
    teletype.addTextToElement(p_element, line_break)
    output_doc.text.addElement(p_element, line_break)
    teletype.addTextToElement(p_element, episode_voices)
    output_doc.text.addElement(p_element, episode_voices)
    teletype.addTextToElement(p_element, line_break)
    output_doc.text.addElement(p_element, line_break)
    teletype.addTextToElement(p_element, line_break)
    output_doc.text.addElement(p_element, line_break)
    # Add the thumbnail
    p = P()
    output_doc.text.addElement(p)
    photoframe = Frame(width="200pt", height="200pt", x="56pt", y="56pt", anchortype="paragraph")
    my_picture = output_doc.addPictureFromString(get_image(episode_thumbnail), mediatype="jpeg")
    photoframe.addElement(Image(href=my_picture))
    p.addElement(photoframe)
    # Page Break
    p_element = P(stylename=p_with_break)
    output_doc.text.addElement(p_element)


# Define styles for the output document
# Title
titleStyle = Style(name="title", family="paragraph")
titleStyle.addElement(ParagraphProperties(attributes={"textalign": "center"}))
titleStyle.addElement(TextProperties(attributes={"fontsize": "14pt"}))
# Subtitle
subtitleStyle = Style(name="subtitle", family="paragraph")
subtitleStyle.addElement(ParagraphProperties(attributes={"textalign": "center"}))
subtitleStyle.addElement(TextProperties(attributes={"fontsize": "24pt"}))
# Paragraph
pStyle = Style(name="paragraph", family="paragraph")
pStyle.addElement(ParagraphProperties(attributes={"textalign": "left"}))
pStyle.addElement(TextProperties(attributes={"fontsize": "12pt"}))
# Date
dateStyle = Style(name="date", family="paragraph")
dateStyle.addElement(ParagraphProperties(attributes={"textalign": "left"}))
dateStyle.addElement(TextProperties(attributes={"fontsize": "12pt"}))
# Paragraph with break_pages
p_with_break = Style(name="WithBreak", parentstylename="Standard", family="paragraph")
p_with_break.addElement(ParagraphProperties(breakbefore="page"))
# Line break
line_break = '\n'

# Compiling RE to clean the HTML in string
remove_html = re.compile('<.*?>')

# Get the podcast page.
page_to_parse = requests.get("https://www.radiokawa.com/episode/ludographie-comparee-1/")
# Change for every podcast
podcast_name = "ludographie_comparee"
parsed_page = BeautifulSoup(page_to_parse.text, features="html.parser")

# Create the output directory if it does not already exists
try:
    os.mkdir(podcast_name)
except FileExistsError:
    print("Output directory already exists")

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
    # document_generation(output_doc, episode_title, episode_subtitle, episode_date, episode_desc, episode_voices,
    #                    episode_thumbnail)
    print("Mise à jour finie. Episode suivant !\n")

os.chdir(podcast_name)
output_doc.save(podcast_name, True)
