import sys
from lxml import etree
import mysql.connector



cnx = mysql.connector.connect(user='root', password='pushka',
                              host='127.0.0.1',
                              database='ocr')
cnx2 = mysql.connector.connect(user='root', password='pushka',
                               host='127.0.0.1',
                               database='ocr')

cnx3 = mysql.connector.connect(user='root', password='pushka',
                               host='127.0.0.1',
                               database='ocr')
cursor = cnx.cursor(buffered=True)
lb_cursor = cnx2.cursor(buffered=True)
list_cursor = cnx3.cursor(buffered=True)

init_query = ('SELECT doc_name FROM ocr.documents group by doc_name')


#TODO: Create list of doc titles
list_cursor.execute(init_query)

doc_names_list = []
for (doc_name) in list_cursor:
    doc_names_list.append(doc_name)

for doc in doc_names_list:
    doc_name = str(doc[0])
    
    lb_query = ("select a.doc_id,a.doc_name,a.word,a.y3,a.y3 - COALESCE(b.y3,0) as DIFF_to_Prev from ocr.documents a LEFT OUTER JOIN ocr.documents b ON (a.doc_id = b.doc_id + 1) WHERE a.doc_name = '%s' order by doc_id" % doc_name)

    cursor.execute(lb_query)

    text = '<lb>'

    for (word) in cursor:
        if word[4] > 20:
                print '</lb><lb>' + str(word[2]) + ' '
                text += '</lb><lb>' + str(word[2]) + ' '
        else:
            print str(word[2])
            text += str(word[2]) + ' '
       
    

        #This section writes the completed TEI string to XML
    tei_string = '<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt><title type="main">%s<lb/></title></titleStmt></fileDesc></teiHeader> <text><p>' % doc_name + text + '</lb></p></text></TEI>'

#    <teiHeader>
#        <fileDesc>
#            <titleStmt>
#                <title type="main">Title of Text<lb/></title>
#            </titleStmt>
#        </fileDesc>
#        </teiHeader> 

    doc = etree.fromstring(tei_string)
    print etree.tostring(doc)


    tree = etree.ElementTree(doc)
    tree.write('{}.xml'.format(doc_name), pretty_print=True, xml_declaration=True,   encoding="utf-8")
    tree.write()