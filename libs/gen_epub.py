from odf.opendocument import OpenDocumentText
from odf.draw import Image, Frame
from odf.style import Style, ParagraphProperties, TextProperties
from odf.text import P
from odf import teletype

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

output_doc.save(podcast_name, True)