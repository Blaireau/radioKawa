import re

def create_output_directory(podcast_name):
    # Create the output directory if it does not already exists
    try:
        os.mkdir(podcast_name)
    except FileExistsError:
        print("Output directory already exists")


def format_date(date_to_clean):
    return date_to_clean[0] + ' : ' + re.sub(remove_html, '', str(date_to_clean[1]))


def format_desc(desc_to_clean):
    return 'Description : ' + re.sub(remove_html, '', str(desc_to_clean[0]))


def format_voices(voices_to_clean):
    out_voices = ''
    for j in voices_to_clean[1:]:
        out_voices += re.sub(remove_html, '', str(j))
    return 'Animateur.trice.s : ' + out_voices


# Compiling RE to clean the HTML in string
remove_html = re.compile('<.*?>')