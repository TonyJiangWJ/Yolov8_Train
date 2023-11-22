import json
import os
import shutil
import label_config


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


def load_label_file(json_path):
    shapeInfos = []
    should_delete = False
    with open(json_path, 'r') as f:
        jsonData = json.load(f)
        # print(str(jsonData['shapes']))
        shapes = jsonData['shapes']
        imagePath = jsonData['imagePath']
        imageHeight = jsonData['imageHeight']
        imageWidth = jsonData['imageWidth']
        # print(f"imagePath: {imagePath} size: {imageWidth}, {imageHeight}")

        for shape in shapes:
            shape_info = ShapeInfo(shape, imagePath, (imageWidth, imageHeight))
            shapeInfos.append(shape_info)
            if (shape_info.label == 'sea_garbage' or shape_info.label == 'sea_ball') and shape_info.top < 800:
                print(f"this file maybe need to delete: {json_path}")
                should_delete = True
        if len(shapes) == 0:
            print(f"this file has no labels need to delete: {json_path}")
            should_delete = True
        f.close()
    if should_delete:
        try:
            os.remove(json_path)
        except:
            print(f"delete file failed: {json_path}")
            pass
    return shapeInfos


## 删除无效的预测数据
def remove_invalid_predict():
    root_path = '../data/forest/predict_with_sea'
    json_files = os.listdir(root_path)
    all_shape_info = []
    labels = set()
    for json_file in json_files:
        if json_file.endswith('json'):
            jsonShapes = load_label_file(os.path.join(root_path, json_file))
            for jsonShape in jsonShapes:
                # print(jsonShape)
                labels.add(jsonShape.label)
                all_shape_info.append(jsonShape)

    for img_file in os.listdir(root_path):
        if img_file.endswith('jpg'):
            json_name = img_file.replace('.jpg', '.json')
            json_path = os.path.join(root_path, json_name)
            if not os.path.exists(json_path):
                print(f'this image has no label: {img_file} delete it')
                os.remove(os.path.join(root_path, img_file))


def overwrite_specific_labeled():
    specific_path = '../data/forest2'
    target_path = '../data/forest/predict'
    recheck_path = '../data/forest2/recheck'
    for json_file in os.listdir(specific_path):
        if json_file.endswith('json'):
            if os.path.exists(os.path.join(target_path, json_file)):
                print(f'has exist: {json_file}')
                shutil.copyfile(os.path.join(specific_path, json_file), os.path.join(target_path, json_file))
                # 复制到recheck文件夹
                shutil.copyfile(os.path.join(specific_path, json_file), os.path.join(recheck_path, json_file))
                shutil.copyfile(os.path.join(specific_path, json_file.replace('json', 'jpg')),
                                os.path.join(recheck_path, json_file.replace('json', 'jpg')))


# 处理原始数据data文件夹下到标签数据
# anylabeling:json => yolo:txt
# anylabeling:json => voc:xml
if __name__ == '__main__':
    overwrite_specific_labeled()
