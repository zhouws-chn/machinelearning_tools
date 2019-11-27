# coding:utf-8
import os
import cv2
from xml.dom.minidom import Document

def check_voc_dirs( voc_path ):
    if not os.path.exists(voc_path):
        os.makedirs(voc_path)
    tmp_path = voc_path+"/Annotations"
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    tmp_path = voc_path + "/ImageSets"
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    tmp_path = voc_path + "/ImageSets/Main"
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    tmp_path = voc_path + "/JPEGImages"
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

def write_xml(filename, saveimg, bboxes, xmlpath):
    doc = Document()
    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)
    folder = doc.createElement('folder')
    folder_name = doc.createTextNode('widerface')
    folder.appendChild(folder_name)
    annotation.appendChild(folder)
    filename_node = doc.createElement('filename')
    filename_name = doc.createTextNode(filename)
    filename_node.appendChild(filename_name)
    annotation.appendChild(filename_node)
    source = doc.createElement('source')
    annotation.appendChild(source)
    database = doc.createElement('database')
    database.appendChild(doc.createTextNode('wider face Database'))
    source.appendChild(database)
    annotation_s = doc.createElement('annotation')
    annotation_s.appendChild(doc.createTextNode('PASCAL VOC2007'))
    source.appendChild(annotation_s)
    image = doc.createElement('image')
    image.appendChild(doc.createTextNode('flickr'))
    source.appendChild(image)
    flickrid = doc.createElement('flickrid')
    flickrid.appendChild(doc.createTextNode('-1'))
    source.appendChild(flickrid)
    owner = doc.createElement('owner')
    annotation.appendChild(owner)
    flickrid_o = doc.createElement('flickrid')
    flickrid_o.appendChild(doc.createTextNode('tdr'))
    owner.appendChild(flickrid_o)
    name_o = doc.createElement('name')
    name_o.appendChild(doc.createTextNode('yanyu'))
    owner.appendChild(name_o)
    size = doc.createElement('size')
    annotation.appendChild(size)
    width = doc.createElement('width')
    width.appendChild(doc.createTextNode(str(saveimg.shape[1])))
    height = doc.createElement('height')
    height.appendChild(doc.createTextNode(str(saveimg.shape[0])))
    depth = doc.createElement('depth')
    depth.appendChild(doc.createTextNode(str(saveimg.shape[2])))
    size.appendChild(width)
    size.appendChild(height)
    size.appendChild(depth)
    segmented = doc.createElement('segmented')
    segmented.appendChild(doc.createTextNode('0'))
    annotation.appendChild(segmented)
    for i in range(0, len(bboxes)):
        bbox = bboxes[i]
        objects = doc.createElement('object')
        annotation.appendChild(objects)
        object_name = doc.createElement('name')
        object_name.appendChild(doc.createTextNode('face'))
        objects.appendChild(object_name)
        pose = doc.createElement('pose')
        pose.appendChild(doc.createTextNode('Unspecified'))
        objects.appendChild(pose)
        truncated = doc.createElement('truncated')
        truncated.appendChild(doc.createTextNode('1'))
        objects.appendChild(truncated)
        difficult = doc.createElement('difficult')
        difficult.appendChild(doc.createTextNode('0'))
        objects.appendChild(difficult)
        bndbox = doc.createElement('bndbox')
        objects.appendChild(bndbox)
        xmin = doc.createElement('xmin')
        xmin.appendChild(doc.createTextNode(str(bbox[0])))
        bndbox.appendChild(xmin)
        ymin = doc.createElement('ymin')
        ymin.appendChild(doc.createTextNode(str(bbox[1])))
        bndbox.appendChild(ymin)
        xmax = doc.createElement('xmax')
        xmax.appendChild(doc.createTextNode(str(bbox[0] + bbox[2])))
        bndbox.appendChild(xmax)
        ymax = doc.createElement('ymax')
        ymax.appendChild(doc.createTextNode(str(bbox[1] + bbox[3])))
        bndbox.appendChild(ymax)
    f = open(xmlpath, 'w')
    f.write(doc.toprettyxml(indent=''))
    f.close()
    pass


root_dir = "/home/ubuntu/Desktop/demo_for_deeplearning/datasheets/raw_widerface"
voc_dir = "/home/ubuntu/Desktop/demo_for_deeplearning/datasheets/voc_widerface"


def convert_imgset(img_set):
    img_dir = root_dir + "/WIDER_" + img_set + "/images"
    gtfile_path = root_dir + "/wider_face_split/wider_face_" + img_set + "_bbx_gt.txt"

    fwrite = open("{}/ImageSets/Main/{}.txt".format(voc_dir, img_set), 'w')
    index = 0

    with open(gtfile_path, 'r') as gtfiles:
        while gtfiles:
            filename = gtfiles.readline()[:-1]
            if (filename == ""):
                break
            img_path = img_dir + '/' + filename
            img = cv2.imread(img_path)
            if img is None:
                continue

            numbbox = int(gtfiles.readline())
            bboxes = []
            for i in range(numbbox):
                line = gtfiles.readline()
                lines = line.split(' ')
                lines = lines[0:4]
                bbox = (int(lines[0]), int(lines[1]), int(lines[2]), int(lines[3]))
                bboxes.append(bbox)
            filename = filename.replace("/", "_")
            if len(bboxes) == 0:
                continue
            cv2.imwrite("{}/JPEGImages/{}".format(voc_dir, filename), img)
            fwrite.write(filename.split(".")[0] + "\n")
            xml_path = "{}/Annotations/{}.xml".format(voc_dir, filename.split(".")[0])
            write_xml(filename, img, bboxes, xml_path)
            print("{}: {}".format(img_set, filename))
        fwrite.close()


if __name__ == "__main__":
    img_sets = ["train", "val"]
    check_voc_dirs(voc_dir)
    for img_set in img_sets:
        convert_imgset(img_set)
    # val.txt > test.txt
    # train.txt > trainval.txt
    os.rename( voc_dir+"/ImageSets/Main"+"/val.txt", voc_dir+"/ImageSets/Main"+"/test.txt" )
    os.rename(voc_dir + "/ImageSets/Main" + "/train.txt", voc_dir + "/ImageSets/Main" + "/trainval.txt")
    print("conver is OK.")
