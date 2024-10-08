import os
import json
import shutil

from lib.mylogger import LOGGER


def get_all_files(root_dir):
    files = []
    for root, dirs, file in os.walk(root_dir):
        for f in file:
            # 是否以.json结尾
            if f.endswith('.json'):
                files.append(os.path.join(root, f))
    LOGGER.info(f"总文件数量：{len(files)}")
    return files


def check_low_confidence(file, target_path):
    global low_count
    with open(file, 'r', encoding='utf-8') as f:
        try:
            content = json.load(f)
        except:
            LOGGER.error(f"Failed to load json file: {file}")
            return
        finally:
            f.close()
    shapes = content['shapes']

    # 使用lambda方式判断shapes中是否存在label=energy_ocr的值，赋值给一个变量
    low_confidence = filter(lambda x: x['score'] is None or x['score'] < 0.8, shapes)
    target_label_list = list(low_confidence)
    target_label = target_label_list[0]['label'] if target_label_list else None
    # has_low_confidence = any(low_confidence)
    # if has_low_confidence is False:
    if target_label is None:
        return
    LOGGER.info(f"Found low confidence in file: {file} label: {target_label} file name: {os.path.basename(file)}")
    target_label_path = os.path.join(target_path, target_label)
    low_count += 1
    if os.path.exists(target_label_path) is False:
        os.mkdir(target_label_path)
    shutil.copyfile(file, os.path.join(target_label_path, os.path.basename(file)))
    if os.path.exists(file.replace('.json', '.jpg')) is False:
        LOGGER.error("Image file not found: " + file.replace('.json', '.jpg'))
        return
    shutil.copyfile(file.replace('.json', '.jpg'), os.path.join(target_label_path, os.path.basename(file).replace('.json', '.jpg')))


if __name__ == '__main__':
    low_count = 0
    # json_files = get_all_files(r'../../../data/forest/predict')
    # json_files = get_all_files(r'Z:\disk2\脚本同步\forest\待标注数据\20240713\predict')
    json_files = get_all_files(r'F:\datasets\ant_forest\20240919')
    target_path = r"../../../data/forest_low_2_merge"
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    os.mkdir(target_path)
    for file in json_files:
        check_low_confidence(file, target_path)
    LOGGER.info(f"总计文件数量：{low_count}")
