#pip install google.cloud, pprint
#pip install lxml==3.6.4
#pip install --upgrade google-api-python-client
#gcloud config set project my-new-default-project

import io
import os
import pprint
from lxml import etree
from collections import defaultdict

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud import language
import mysql.connector

cnx = mysql.connector.connect(user='root', password='pushka',
                              host='127.0.0.1',
                              database='dl_ocr')
cnx2 = mysql.connector.connect(user='root', password='pushka',
                               host='127.0.0.1',
                               database='dl_ocr')


cursor = cnx.cursor(buffered=True)
cursor2 = cnx2.cursor(buffered=True)

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

file_name_1 = '"' + str(file_name.split('/', -1)[-1]) + '"'


# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()
    image = vision_client.image(
        content=content)


# Performs label detection on the image file
labels = image.detect_text()

#!! labels[0] is the whole text, all later list items are individual word tokens

for label in labels[1:]:
    print(label._description)
    word_1 = label._description
    word = '"' + word_1 + '"'
    text = language_client.document_from_text(word_1)
    
    entity_response = text.analyze_entities()
    #for entity in entity_response.entities:
    try: 
        entity_type_1 = entity_response.entities[0].entity_type 
        entity_type = '"' + entity_type_1 + '"'        
    except (IndexError):
        entity_type = '"' + '"'
        
    x0 = label.bounds.vertices[0].x_coordinate
    y0 = label.bounds.vertices[0].y_coordinate
            
    x1 = label.bounds.vertices[1].x_coordinate
    y1 = label.bounds.vertices[1].y_coordinate
            
    x2 = label.bounds.vertices[2].x_coordinate
    y2 = label.bounds.vertices[2].y_coordinate
            
    x3 = label.bounds.vertices[3].x_coordinate
    y3 = label.bounds.vertices[3].y_coordinate    
        
         
    doc_name_query = ("INSERT dl_ocr.documents (doc_name,word,entity_type,x0,y0,x1,y1,x2,y2,x3,y3) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);" % (file_name_1,word,entity_type,x0,y0,x1,y1,x2,y2,x3,y3)) 
    
    cursor.execute(doc_name_query)
    cnx.commit()
    
    
    

print "Hi there!"       
        
        
        
        
#print (etree.tostring(tei, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
#print (repr(etree.tostring(tei, pretty_print=True, xml_declaration=True, encoding='UTF-8')))


#Save file as xml        
#outFile = open('test_tei.xml', 'w')
#tei.write(outFile)

tree = etree.ElementTree(tei)
tree.write('output.xml', pretty_print=True, xml_declaration=True,   encoding="utf-8")
    
