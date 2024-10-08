import os
import shutil
from lib.mylogger import LOGGER


def copy_labeled_data(json_source_path, img_source_path, target_path, overwrite, _copy_count):
    if not os.path.exists(json_source_path):
        LOGGER.warn(f"{json_source_path} not exists")
        return _copy_count
    if not os.path.exists(target_path):
        os.mkdir(target_path)

    # 遍历数据集目录，将已标注数据复制到工程目录到data目录下
    # 后续执行convert_xml2json和split构建训练集数据
    files = os.listdir(json_source_path)
    for file in files:
        if os.path.isdir(json_source_path + '/' + file):
            print(f"dir {json_source_path + '/' + file}")
            _copy_count = copy_labeled_data(json_source_path + '/' + file, img_source_path + '/' + file, target_path,
                                             overwrite, _copy_count)
            continue
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
    json_root_path = r'../data/forest_low_2_merge'
    # json_root_path = r'F:\datasets\manor\predict'
    # json_root_path = r'Z:\disk2\脚本同步\forest\待标注数据\20240714\predict'

    # json_root_path = r'Z:\disk2\脚本同步\forest\待标注数据\20240716/'
    # json_root_path = r'H:\Projects\repository\datasets\ant_forest/'
    # json_root_path = r'H:\Projects\repository\datasets\ant_forest\20240629\93860e8d414b61e9b0018f47aed97282\2024-06-28/'
    # json_root_path = r'H:\Projects\repository\datasets\manor_games\ball/'
    # json_root_path = r'../data/forest/recheck'
    img_root_path = json_root_path
    target_data_path = r'../data/forest_20240717'
    # target_data_path = r'E:/Repository/YOLOV8_train/data/forest_20240625'
    # 如果目录不存在，则创建目录，如果父级目录不存在则将父级目录一起创建
    if not os.path.exists(target_data_path):
        os.makedirs(target_data_path, exist_ok=True)

    # for dir_name in ['friend_no_energy', 'home', 'one_key', 'sea_ball', 'sea_ball_friend']:
    # for dir_name in ['backpack', 'collect', 'countdown', 'item', 'magic_species', 'reward', 'sea_garbage', 'sea_ocr', 'stroll_btn']:
    # for dir_name in ['sea_ocr', 'sea_garbage', 'cooperation', 'gift']:
    for dir_name in ['']:
        copy_count = copy_labeled_data(json_root_path + dir_name, img_root_path + dir_name, target_data_path,
                                       overwrite=True,
                                       _copy_count=copy_count)
    print(f'复制了{copy_count}个标注数据')
