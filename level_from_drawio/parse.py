import xml.etree.ElementTree as ET
from dataclasses import fields
from operator import attrgetter
from course import Course, Element

# https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree

course = Course()

tree = ET.parse("drawio.xml")
root = tree.getroot()[0][0][0]

def get_style(cell):
    style = cell.get("style").split(";")[0]
    return style if "=" not in style else "rectangle"

for cell in root:
    try:
        geometry = cell[0]
    except IndexError:
        continue
    if cell.get("value") == "COURSE":
        course.width = int(geometry.get("width"))
        course.height = int(geometry.get("height"))
    else:
        elem = Element(
            **{k: int(v) for k, v in geometry.attrib.items() if k in list(map(attrgetter("name"), fields(Element)))},
            style=get_style(cell)
        )
        course.elements.append(elem)
        if cell.get("value") == "SPAWN":
            course.spawn = elem
        elif cell.get("value") == "HOLE":
            course.hole = elem
        
print(course.__dict__)
course.validate()
course.show()
