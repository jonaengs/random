import xml.etree.ElementTree as ET
from dataclasses import fields
from course import Course, Element
from pprint import pprint

# https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree

def get_styles(cell):
    styles = cell.get("style").split(";")
    return {
        "shape": styles[0] if "=" not in styles[0] else "rectangle",
        "rotation": next((int(s.split("=")[1]) for s in styles if s.startswith("rotation")), 0)
    }

def parse(file):
    course = Course()
    tree = ET.parse(file)
    root = tree.getroot()[0][0][0]

    for cell in root:
        if not cell:  # cell has no children
            continue

        geometry = cell[0]
        if cell.get("value") == "COURSE":
            course.width, course.height = int(geometry.get("width")), int(geometry.get("height"))
        else:
            elem = Element(
                **{k: int(v) for k, v in geometry.attrib.items() if k in Element.field_names()},
                **get_styles(cell),
                function=cell.get("value").lower()
            )
            course.elements.append(elem)

    pprint(course.__dict__)
    course.validate()        
    return course
    
if __name__ == '__main__':
    parse("drawio.xml").show()
