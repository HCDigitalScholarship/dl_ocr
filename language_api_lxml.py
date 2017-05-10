#pip install google.cloud, pprint
#pip install lxml==3.6.4
#pip install --upgrade google-api-python-client
#gcloud config set project my-new-default-project

import io
import os
import pprint
from lxml import etree

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud import language

# prepare TEI document
tei = etree.Element('TEI', xmlns='http://www.tei-c.org/ns/1.0')
tei_header = etree.SubElement(tei, 'teiHeader')
filedesc = etree.SubElement(tei_header, 'fileDesc')
file_titlestmt = etree.SubElement(filedesc, 'titleStmt')
titlemain = etree.SubElement(file_titlestmt, 'title', type='main')


## VISION API SECTION
# Instantiates a client
vision_client = vision.Client()

# Instantiates a client
language_client = language.Client()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    '/Users/ajanco/Downloads/Untitled/Untitled-5.jpg')


# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()
    image = vision_client.image(
        content=content)


# Performs label detection on the image file
labels = image.detect_text()

#!! labels[0] is the whole text, all later list items are individual word tokens


root = etree.SubElement(tei, 'text')
root.text = labels[0].description
#labels[0].description.replace('\n','<lb>')

#for label in labels[1:]:
    #print(label._description)
#    text = language_client.document_from_text(label.description)
#    entity_response = text.analyze_entities()
#    for entity in entity_response.entities:
        #print entity.name,entity.entity_type
        
#        root = etree.SubElement(tei, str(entity.entity_type))
#        root.text = str(entity.name)
        
        #google.cloud.language.document.Document (sentences[list], tokens[list],sentiment, entities[list], language)
        #This is the location data from vision
        #for vertex in label.bounds.vertices:
        #    print vertex.x_coordinate, vertex.y_coordinate 
        
#print (etree.tostring(tei, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
#print (repr(etree.tostring(tei, pretty_print=True, xml_declaration=True, encoding='UTF-8')))


#Save file as xml        
#outFile = open('test_tei.xml', 'w')
#tei.write(outFile)

tree = etree.ElementTree(tei)
tree.write('output.xml', pretty_print=True, xml_declaration=True,   encoding="utf-8")
    
