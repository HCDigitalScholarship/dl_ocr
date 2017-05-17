import sys
from lxml import etree


milne = '''<TEI>
<text>
<!-- frontmatter -->
<pb n="6"/>
<p>
  PARECER<lb/>
  DEL R. PADRE PREDICADOR FRA
  Migue Pantaleon, Maeſtro de Novictos, y<lb/>
  Compañero del M. R. P. M. Fr. Leonardo<lb/>
  Levanto, digniſsimo Prior Provincil de eſta<lb/>
  Provincia de San Miguel, y Santos Angeles de<lb/>
  La Puebla de los Angeles de Sagrado Orden de<lb/>
  Predicadores.<lb/>
  Excelentiſsimo Señor.
</p></text>
</TEI>'''
doc = etree.fromstring(milne)
print etree.tostring(doc)


tree = etree.ElementTree(doc)
tree.write('experiment.xml', pretty_print=True, xml_declaration=True,   encoding="utf-8")