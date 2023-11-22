import os
import shutil

def copy_labeled_data(json_source_path, img_source_path, target_path, overwrite, _copy_count):
    if not os.path.exists(target_path):
        os.mkdir(target_path)

    # 遍历数据集目录，将已标注数据复制到工程目录到data目录下
    # 后续执行convert_xml2json和split构建训练集数据
    files = os.listdir(json_source_path)
    for file in files:
        if file.endswith('json'):
            json_path = os.path.join(json_source_path, file)
            target_json_path = os.path.join(target_path, file)
            img_path = os.path.join(img_source_path, file.replace('json', 'jpg'))
            target_img_path = target_json_path.replace('json', 'jpg')
            if not os.path.exists(img_path):
                # 不是有效的json文件
                continue
            if overwrite or not os.path.exists(target_json_path):
                shutil.copyfile(json_path, target_json_path)
                print(f"复制 {json_path} => {target_json_path}")
                _copy_count += 1

            if overwrite or not os.path.exists(target_img_path):
                shutil.copyfile(img_path, target_img_path)
                print(f"复制 {img_path} => {target_img_path}")
    return _copy_count


if __name__ == '__main__':
    copy_count = 0
    json_root_path = r'H:/Projects/repository/datasets/ant_forest/'
    img_root_path = json_root_path
    # json_root_path = 'K:/YOLOV8_train_clean/data/'
    # img_root_path = 'K:/YOLOV8_train_clean/data/'
    # target_data_path = 'K:/YOLOV8_train_clean/data/yuanshen_temple'
    target_data_path = 'K:/YOLOV8_train_clean/data/forest3'
    for dir_name in ['merge202308-10']:
        copy_count = copy_labeled_data(json_root_path + dir_name, img_root_path + dir_name, target_data_path,
                                       overwrite=False,
                                       _copy_count=copy_count)
    print(f'复制了{copy_count}个标注数据')
