from writer.annotation import Object

class COCOWriter:
    def __init__(self):
        pass
    
    def write(self, annotation, file, classes):
        file = open(file, 'w+')
        for obj in annotation.objects:
            class_id = classes.index(obj.name)
            box_width = float(obj.xmax - obj.xmin)
            box_height = float(obj.ymax - obj.ymin)
            x_center = (obj.xmin + (box_width / 2.))
            y_center = (obj.ymin + (box_height / 2.))
            file.write(f'{class_id} {x_center / annotation.width } {y_center / annotation.height} {box_width / annotation.width } {box_height / annotation.height}\n')
            
            