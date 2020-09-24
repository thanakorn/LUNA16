from voc.writer import VOCWriter
from voc.annotation import Annotation, Size, Object

if __name__=='__main__':
    writer = VOCWriter()
    size = Size(100, 100, 3)
    annotation = Annotation('folder', 'file', 'path', 'db', size)
    annotation.add_object(Object('nodule', (233, 89), (386, 262)))
    annotation.add_object(Object('nodule', (323, 809), (86, 262)))
    writer.write(annotation, 'output.xml')