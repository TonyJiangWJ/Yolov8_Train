import json
import os
import xml.etree.ElementTree as ET
import shutil
import label_config
import dataset_sql
from lib.mylogger import LOGGER


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
        if _shape.__contains__('group_id'):
            self.group_id = _shape['group_id']
        else:
            self.group_id = None
        points = _shape['points']
        if len(points) == 4:
            self.left = points[0][0]
            self.top = points[0][1]
            self.right = points[2][0]
            self.bottom = points[2][1]
        else:
            self.left = points[0][0]
            self.top = points[0][1]
            self.right = points[1][0]
            self.bottom = points[1][1]
        self.image_id = image_id
        self.image_size = image_size
        self.points = points

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


def load_label_file(json_path, create_voc_xml=False):
    shapeInfos = []
    with open(json_path, 'r', encoding='utf-8') as f:
        jsonData = json.load(f)
        print(str(jsonData['shapes']))
        shapes = jsonData['shapes']
        imagePath = jsonData['imagePath']
        imageHeight = jsonData['imageHeight']
        imageWidth = jsonData['imageWidth']
        print(f"imagePath: {imagePath} size: {imageWidth}, {imageHeight}")
        if create_voc_xml:
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
    return shapeInfos, imagePath


def ensure_datasets_dir(dataset_root, overwrite_all, images_path, labels_path):
    if not os.path.exists(dataset_root):
        os.makedirs(dataset_root)
    if overwrite_all:
        shutil.rmtree(images_path, ignore_errors=True)
        shutil.rmtree(labels_path, ignore_errors=True)
    if not os.path.exists(images_path):
        os.makedirs(images_path)
    if not os.path.exists(labels_path):
        os.makedirs(labels_path)


def load_json_and_copy_data(root_path, dataset, conn, specific_labels, overwrite_all, label_counter):
    json_files = os.listdir(root_path)
    labels = set()
    all_shape_info = []
    total = len(json_files)
    current = 0
    for json_file in json_files:
        current += 1
        if json_file.endswith('json'):
            image_id = json_file.replace('.json', '')
            json_shapes, image_path = load_label_file(os.path.join(root_path, json_file))
            dataset_image = dataset_sql.DatasetImages(dataset.id, image_id, image_path)
            dataset_image.save(conn)
            for jsonShape in json_shapes:
                print(jsonShape)
                labels.add(jsonShape.label)
                all_shape_info.append(jsonShape)
        if current % 10 == 0:
            print(f"{current / total * 100:.2f}%")
    labels = sorted(list(labels))
    print(f"data labels: {labels}")
    if len(specific_labels) > 0 and len(labels):
        not_exists_labels = sorted(list(set(labels) - set(specific_labels)))
        print(f'not exists labels: {not_exists_labels}')
        labels = specific_labels + not_exists_labels
    print(f"using labels: {labels}")

    grouped_labels = {}
    for shapeInfo in all_shape_info:
        image_id = shapeInfo.image_id
        if image_id not in grouped_labels:
            grouped_labels[image_id] = []
        grouped_labels[image_id].append(shapeInfo)

    # 打印分组数据 并将json转换为yolo txt格式
    for image_id, group_items in grouped_labels.items():
        print(f"image id: {image_id}")
        txt_file_name = image_id.replace('jpg', 'txt')
        txt_file = os.path.join(root_path, txt_file_name)
        if overwrite_all is False:
            if os.path.exists(txt_file):
                LOGGER.verbose(f"skip exists txt file: {txt_file}")
                continue
        with open(txt_file, 'w') as fw:
            for shapeInfo in group_items:
                print(shapeInfo.to_yolo_txt(labels))
                if shapeInfo.label not in label_counter:
                    label_counter[shapeInfo.label] = 0
                label_counter[shapeInfo.label] += 1
                fw.write(shapeInfo.to_yolo_txt(labels) + '\n')
            fw.close()
    return list(labels)


def copy_dataset_to_target_path(root_path, images_path, labels_path, overwrite_all, copied_image_ids, limit):
    data_files = os.listdir(root_path)
    count = 0
    for data_file in data_files:
        data_file_path = os.path.join(root_path, data_file)
        if data_file.endswith("txt"):
            image_file_path = data_file_path.replace("txt", "jpg")
            if os.path.exists(image_file_path) is False:
                os.remove(data_file_path)
                continue
            if overwrite_all or os.path.exists(os.path.join(labels_path, data_file)) is False:
                copied_image_ids.append(data_file.replace('.txt', ''))
                print(f"copy {data_file_path} to {labels_path}/{data_file}")
                shutil.copyfile(data_file_path, os.path.join(labels_path, data_file))
            if overwrite_all or os.path.exists(os.path.join(images_path, data_file.replace('txt', 'jpg'))) is False:
                print(f"copy {image_file_path} to {images_path}/{data_file.replace('txt', 'jpg')}")
                shutil.copyfile(image_file_path, os.path.join(images_path, data_file.replace('txt', 'jpg')))
            count += 1
            if limit is not None and count >= limit:
                break


def summary_labels(dataset, conn, overwrite_all, labels, labels_chz, copied_image_ids):
    dataset_sql.check_json_labels_and_save(dataset, conn, overwrite=overwrite_all, filter_image_ids=copied_image_ids)
    # 统计标签数据
    label_group_counter = {}
    dataset_sql.summary_dataset_labels(dataset, labels, labels_chz, conn, label_group_counter)
    print(f"all labels: {labels}")
    print("for yml:")
    idx = 0
    for label in labels:
        print(f'{idx}: {label}')
        idx += 1
    print("当前数据集的标签统计：", len(labels))
    for label in labels:
        if label in label_group_counter:
            print(f"{label}: {label_group_counter[label]}")


def convert_to_yolo_txt(specific_labels, labels_chz, dataset_name, root_path=None, target_path=None, max_predict=None,
                        overwrite=True):
    # 是否指定最大处理数量
    limit = max_predict
    # 是否覆盖已存在的图片和标注数据
    overwrite_all = overwrite
    if root_path is None:
        root_path = f'./data/{dataset_name}'
    if target_path is None:
        target_path = f'./datasets/{dataset_name}'
    images_path = os.path.join(target_path, 'images')
    labels_path = os.path.join(target_path, 'labels')
    dataset = dataset_sql.Dataset(dataset_name, root_path)
    conn = dataset_sql.create_sqlite_connection()
    dataset.save(conn)
    ensure_datasets_dir(target_path, overwrite_all, images_path, labels_path)

    labels = []
    copied_image_ids = []
    label_counter = {}

    specific_labels = load_json_and_copy_data(root_path, dataset, conn, specific_labels, overwrite_all, label_counter)
    copy_dataset_to_target_path(root_path, images_path, labels_path, overwrite_all, copied_image_ids, limit)

    summary_labels(dataset, conn, overwrite_all, specific_labels, labels_chz, copied_image_ids)


# 处理原始数据data文件夹下到标签数据
# anylabeling:json => yolo:txt
# anylabeling:json => voc:xml
if __name__ == '__main__':
    # 是否指定最大处理数量
    max_predict = None
    # 是否覆盖已存在的图片和标注数据
    overwrite = False
    # 初始化训练集时，指定为空数组，将自动统计并打印所有标签
    # specific_labels = []
    # labels_chz = []
    specific_labels = label_config.to_list(label_config.ant_forest)
    labels_chz = label_config.to_list(label_config.ant_forest_chz)
    # 指定
    dataset_name = 'forest_20240717'
    convert_to_yolo_txt(specific_labels, labels_chz, dataset_name,
                        max_predict=max_predict, overwrite=overwrite)
