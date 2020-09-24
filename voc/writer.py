import xml.etree.ElementTree as et
from copy import deepcopy

class VOCWriter:
    def __init__(self):
        self.annotation_template = et.parse('./templates/annotation.xml')
        self.object_template = et.parse('./templates/object.xml')       
    
    def write(self, annotation, file):
        output = deepcopy(self.annotation_template).getroot()
        output.find('folder').text = annotation.folder
        output.find('filename').text = annotation.filename
        output.find('path').text = annotation.path
        output.find('source').find('database').text = annotation.database
        output.find('size').find('width').text = str(annotation.width)
        output.find('size').find('height').text = str(annotation.height)
        output.find('size').find('depth').text = str(annotation.depth)
        
        for obj in annotation.objects:
            obj_output = deepcopy(self.object_template).getroot()
            obj_output.find('name').text = obj.name
            obj_output.find('pose').text = obj.pose
            obj_output.find('truncated').text = str(obj.truncated)
            obj_output.find('difficult').text = str(obj.difficult)
            obj_output.find('bndbox').find('xmin').text = str(obj.xmin)
            obj_output.find('bndbox').find('ymin').text = str(obj.ymin)
            obj_output.find('bndbox').find('xmax').text = str(obj.xmax)
            obj_output.find('bndbox').find('ymax').text = str(obj.ymax)
            output.append(obj_output)
        
        tree = et.ElementTree(output)
        tree.write(file)