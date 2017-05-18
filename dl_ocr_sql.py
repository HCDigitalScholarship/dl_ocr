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
                              database='ocr')
cnx2 = mysql.connector.connect(user='root', password='pushka',
                               host='127.0.0.1',
                               database='ocr')


cursor = cnx.cursor(buffered=True)
cursor2 = cnx2.cursor(buffered=True)


## VISION API SECTION
# Instantiates a client
#vision_client = vision.Client()
vision_client = vision.Client.from_service_account_json('/Users/ajanco/projects/46270ee61e5d.json')

# Instantiates a client
language_client = language.Client()

#this finds the last entry in the database and sets the start of the loop at that file
files_list = []
for fn in os.listdir('/Users/ajanco/projects/dl_ocr/DQB/images/'):
    
    files_list.append(fn)
    
end = len(files_list) 
#Get filename of last record in the db
query = ("SELECT doc_id, doc_name FROM ocr.documents WHERE doc_id = (SELECT MAX(doc_id) FROM dl_ocr.documents);")
cursor.execute(query)

#This finds the index for the file in the list of filenames 
for (doc_name) in cursor:
    get_this = doc_name[1]

try:
    i = files_list.index(get_this)
except (NameError):
    i = 1
    
for file in files_list[i:end]:

    file_name = "/Users/ajanco/projects/dl_ocr/DQB/images/" + file

    file_name_1 = '"' + str(file) + '"'
    #file_name_2 = str(file_name.split('/', -1)[-1])

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
            if '"' in word_1:
                word_1.replace('"','\"')
    
            else:
                word = '"' + word_1 + '"'
                text = language_client.document_from_text(word_1)
    
                #RIP Natural Language API call, entity_response = text.analyze_entities()
                #try: 
                #    entity_type_1 = entity_response.entities[0].entity_type 
                #    entity_type = '"' + entity_type_1 + '"'        
                #except (IndexError):
                #    entity_type = '"' + '"'
        
            x0 = label.bounds.vertices[0].x_coordinate
            y0 = label.bounds.vertices[0].y_coordinate
            
            x1 = label.bounds.vertices[1].x_coordinate
            y1 = label.bounds.vertices[1].y_coordinate
            
            x2 = label.bounds.vertices[2].x_coordinate
            y2 = label.bounds.vertices[2].y_coordinate
            
            x3 = label.bounds.vertices[3].x_coordinate
            y3 = label.bounds.vertices[3].y_coordinate    
            
            try:
                doc_name_query = ("INSERT ocr.documents (doc_name,word,x0,y0,x1,y1,x2,y2,x3,y3) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);" % (file_name_1,word,entity_type,x0,y0,x1,y1,x2,y2,x3,y3)) 
    
                cursor.execute(doc_name_query)
                cnx.commit()
                
            except:
                doc_name_query = ("INSERT ocr.documents (doc_name,word,x0,y0,x1,y1,x2,y2,x3,y3) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);" % (file_name_1,word,x0,y0,x1,y1,x2,y2,x3,y3)) 
                cursor.execute(doc_name_query)
                cnx.commit()                
            
