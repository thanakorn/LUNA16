from writer.annotation import Object

class COCOWriter:
    def __init__(self):
        pass
    
    def write(self, annotation, file, classes):
        file = open(file, 'w+')
        for obj in annotation.objects:
            class_id = classes.index(obj.name)
            box_width = float(obj.xmax - obj.xmin) / annotation.width
            box_height = float(obj.ymax - obj.ymin) / annotation.height
            x_center = (obj.xmin + (box_width / 2.)) / annotation.width
            y_center = (obj.ymin + (box_height / 2.)) / annotation.height
            file.write(f'{class_id} {x_center} {y_center} {box_width} {box_height}')
            
            