import os
import xml.etree.ElementTree as ET
import treetaggerwrapper as ttw
import re

files = []

path_of_the_directory = './files/'

object = os.scandir(path_of_the_directory)
print("Scanning files")
for n in object:
    if n.is_dir() or n.is_file():
        files.append(n.name)
object.close()
print(len(files), 'files found')


def convert(xml_name, xml_file_location):

    result_file_name = re.sub('[^0-9a-zA-Z]+', '_', xml_name)
    file_id = result_file_name.replace('_xml', '').upper()
    res_path = './result/'

    tree = ET.parse(xml_file_location + xml_name)
    root = tree.getroot()

    for child in root:
        if child.tag == 'header':
            root.remove(child)

    # set tag name as their role
    for s in root.iter("segment"):
        try:
            s.tag = s.attrib['role']
        except KeyError:
            # print(s.attrib['id'])
            s.tag = s.attrib['features'].split(';')[-1]
        # remove unnecessary attributes
        s.attrib.pop('id', None)
        s.attrib.pop('features', None)
        s.attrib.pop('state', None)
        s.attrib.pop('parent', None)
        s.attrib.pop('role', None)

    # convert into string and modify
    xml_string = ET.tostring(root).decode()
    text = re.sub(r'&#[0-9]+;', '', xml_string)
    a = text.replace('<body>', '')
    b = a.replace('</body>', '')
    c = b.replace('document', 'text')
    d = c.replace('<???>', '')
    e = d.replace('</???>', '')
    fin_str = e.replace('<text>', '<text id="'+file_id+'">')

    tagger = ttw.TreeTagger(TAGLANG='en', TAGOPT='-token -lemma -sgml')
    tags= tagger.tag_text(fin_str)
    mt_string = ''

    for string in tags:
        mt_string += string + '\n'

    e = mt_string.replace('<unknown>', '')

    text_file = open(res_path + result_file_name.replace('_xml', '_tagged.xml'), 'w')

    text_file.write(e)

    text_file.close()
    print(file_id)


print('====Converting in progress =====')

for n in files:
    convert(n, path_of_the_directory)

print('Finished !')
