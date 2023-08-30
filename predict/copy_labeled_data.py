import os
import shutil

json_root_path = 'H:/Projects/repository/datasets/feed'
img_root_path = 'H:/Projects/repository/datasets/feed'
target_data_path = 'K:/YOLOV8_train_clean/data/feed'
if not os.path.exists(target_data_path):
    os.mkdir(target_data_path)

# 遍历数据集目录，将已标注数据复制到工程目录到data目录下
# 后续执行convert_xml2json和split构建训练集数据
files = os.listdir(json_root_path)
for file in files:
    if file.endswith('json'):
        json_path = os.path.join(json_root_path, file)
        target_json_path = os.path.join(target_data_path, file)
        if not os.path.exists(target_json_path):
            shutil.copyfile(json_path, target_json_path)
            print(f"复制 {json_path} => {target_json_path}")

        img_path = os.path.join(img_root_path, file.replace('json', 'jpg'))
        target_img_path = target_json_path.replace('json', 'jpg')
        if not os.path.exists(target_img_path):
            shutil.copyfile(img_path, target_img_path)
            print(f"复制 {img_path} => {target_img_path}")
