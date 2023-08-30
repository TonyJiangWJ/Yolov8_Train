import json
import os
import xml.etree.ElementTree as ET
import shutil


def convertYolo(size, box):
    left, top, right, bottom = box
    width, height = size
    x_center = (left + right) / 2.0
    y_center = (top + bottom) / 2.0
    rx = x_center / width
    ry = y_center / height
    rw = (right - left) / width
    rh = (bottom - top) / height
    return rx, ry, rw, rh


def convertVoc(data):
    # 定义 VOC XML 文件的根节点
    root = ET.Element('annotation')

    # 添加文件名元素
    filename = ET.SubElement(root, 'filename')
    filename.text = data['imagePath']  # 替换为实际的图像文件名

    # 添加图像尺寸元素
    size = ET.SubElement(root, 'size')
    width = ET.SubElement(size, 'width')
    width.text = str(data['imageWidth'])  # 替换为实际图像宽度
    height = ET.SubElement(size, 'height')
    height.text = str(data['imageHeight'])  # 替换为实际图像高度

    # 遍历 JSON 数据中的标注对象
    for annotation in data['shapes']:
        # 获取标注的类别和边界框信息
        label = annotation['label']
        points = annotation['points']
        x_min = min(p[0] for p in points)
        y_min = min(p[1] for p in points)
        x_max = max(p[0] for p in points)
        y_max = max(p[1] for p in points)

        # 创建对象元素
        obj = ET.SubElement(root, 'object')
        name = ET.SubElement(obj, 'name')
        name.text = label
        difficult = ET.SubElement(obj, 'difficult')
        difficult.text = '0'

        # 创建边界框元素
        bndbox = ET.SubElement(obj, 'bndbox')
        xmin = ET.SubElement(bndbox, 'xmin')
        xmin.text = str(int(x_min))
        ymin = ET.SubElement(bndbox, 'ymin')
        ymin.text = str(int(y_min))
        xmax = ET.SubElement(bndbox, 'xmax')
        xmax.text = str(int(x_max))
        ymax = ET.SubElement(bndbox, 'ymax')
        ymax.text = str(int(y_max))

    # 将 ElementTree 转换为字符串
    xml_string = ET.tostring(root, encoding='utf8', method='xml')

    # 打印字符串
    return xml_string.decode('utf8')


class ShapeInfo:
    def __init__(self, _shape, image_id, image_size):
        self.label = _shape['label']
        self.shape_type = _shape['shape_type']
        self.group_id = _shape['group_id']
        points = _shape['points']
        self.left = points[0][0]
        self.top = points[0][1]
        self.right = points[1][0]
        self.bottom = points[1][1]
        self.image_id = image_id
        self.image_size = image_size

    def __str__(self):
        dump = dict()
        dump['label'] = self.label
        dump['shape_type'] = self.shape_type
        dump['group_id'] = self.group_id
        dump['left'] = self.left
        dump['top'] = self.top
        dump['right'] = self.right
        dump['bottom'] = self.bottom
        return json.dumps(dump)

    def to_yolo_txt(self, labels):
        cls_id = labels.index(self.label)
        yolo_array = convertYolo(self.image_size, (self.left, self.top, self.right, self.bottom))
        return f"{cls_id} {' '.join(str(a) for a in yolo_array)}"

    def to_voc_xml(self):
        pass


def load_label_file(json_path):
    shapeInfos = []
    with open(json_path, 'r') as f:
        jsonData = json.load(f)
        print(str(jsonData['shapes']))
        shapes = jsonData['shapes']
        imagePath = jsonData['imagePath']
        imageHeight = jsonData['imageHeight']
        imageWidth = jsonData['imageWidth']
        print(f"imagePath: {imagePath} size: {imageWidth}, {imageHeight}")
        voc_file_name = imagePath.replace('jpg', 'xml')
        voc_file_name = os.path.join(os.path.dirname(json_path), voc_file_name)
        print("voc xml: " + voc_file_name)
        xml_str = convertVoc(jsonData)
        with open(voc_file_name, 'w') as fw:
            fw.write(xml_str)
            fw.close()
        for shape in shapes:
            shape_info = ShapeInfo(shape, imagePath, (imageWidth, imageHeight))
            shapeInfos.append(shape_info)
        f.close()
    return shapeInfos


def ensure_datasets_dir(dataset_root):
    if not os.path.exists(dataset_root):
        os.makedirs(dataset_root)
    if not os.path.exists(images_path):
        os.makedirs(images_path)
    if not os.path.exists(labels_path):
        os.makedirs(labels_path)


# 处理原始数据data文件夹下到标签数据
# anylabeling:json => yolo:txt
# anylabeling:json => voc:xml
if __name__ == '__main__':
    # specific_labels = ['booth_btn', 'collect_coin', 'collect_egg', 'collect_food', 'cook', 'countdown', 'donate',
    #                    'eating_chicken', 'employ', 'empty_booth', 'feed_btn', 'friend_btn', 'has_food', 'has_shit',
    #                    'hungry_chicken', 'item', 'kick-out', 'no_food', 'not_ready', 'operation_booth', 'plz-go',
    #                    'punish_booth', 'punish_btn', 'signboard', 'sleep', 'speedup', 'sports', 'stopped_booth',
    #                    'thief_chicken']
    specific_labels = []
    root_path = './data/feed'
    target_path = './datasets/feed'
    images_path = os.path.join(target_path, 'images')
    labels_path = os.path.join(target_path, 'labels')
    ensure_datasets_dir(target_path)
    json_files = os.listdir(root_path)
    all_shape_info = []
    labels = set()
    for json_file in json_files:
        if json_file.endswith('json'):
            jsonShapes = load_label_file(os.path.join(root_path, json_file))
            for jsonShape in jsonShapes:
                print(jsonShape)
                labels.add(jsonShape.label)
                all_shape_info.append(jsonShape)
    labels = sorted(list(labels))
    print(f"data labels: {labels}")
    if len(specific_labels) > 0:
        labels = specific_labels
    print(f"using labels: {labels}")

    grouped_labels = {}
    for shapeInfo in all_shape_info:
        image_id = shapeInfo.image_id
        if image_id not in grouped_labels:
            grouped_labels[image_id] = []
        grouped_labels[image_id].append(shapeInfo)
    # 打印分组数据
    for image_id, group_items in grouped_labels.items():
        print(f"image id: {image_id}")
        txt_file_name = image_id.replace('jpg', 'txt')
        txt_file = os.path.join(root_path, txt_file_name)
        with open(txt_file, 'w') as fw:
            for shapeInfo in group_items:
                print(shapeInfo.to_yolo_txt(labels))
                fw.write(shapeInfo.to_yolo_txt(labels) + '\n')
            fw.close()

    data_files = os.listdir(root_path)
    for data_file in data_files:
        data_file_path = os.path.join(root_path, data_file)
        if data_file.endswith("txt"):
            image_file_path = data_file_path.replace("txt", "jpg")
            print(f"copy {data_file_path} to {labels_path}/{data_file}")
            shutil.copyfile(data_file_path, os.path.join(labels_path, data_file))
            print(f"copy {image_file_path} to {images_path}/{data_file.replace('txt', 'jpg')}")
            shutil.copyfile(image_file_path, os.path.join(images_path, data_file.replace('txt', 'jpg')))

    print(f"all labels: {labels}")
    print("for yml:")
    idx = 0
    for label in labels:
        print(f'{idx}: "{label}"')
        idx += 1
