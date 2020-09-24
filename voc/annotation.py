class Annotation:
    def __init__(self, folder, filename, path, database, size, segmented=0):
        self.folder = folder
        self.filename = filename
        self.path = path
        self.database = database
        self.width, self.height, self.depth = size
        self.segmented = segmented
        self.objects = []
        
    def add_object(self, obj):
        self.objects.append(obj)

class Object:
    def __init__(self, name, xy_min, xy_max, pose='Unspecified', truncated=0, difficult=0):
        self.name = name
        self.pose = pose
        self.truncated = truncated
        self.xmin, self.ymin = xy_min
        self.xmax, self.ymax = xy_max
        self.difficult = difficult