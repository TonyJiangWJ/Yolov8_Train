import json
import os
import shutil

from lib.mylogger import LOGGER
from train.win_power_control import allow_sleep, prevent_sleep

from remove_invalid_labels import get_all_files, check_and_save_target

def check_and_remvoe_target(file, label):
    with open(file, 'r', encoding='utf-8') as f:
        content = json.load(f)
        f.close()
    shapes = content['shapes']
    if any(filter(lambda x: x['label'] == label, shapes)):
        LOGGER.info(f"find target label[{label}] in {file}")
        try:
            os.remove(file)
            os.remove(file.replace('.json', '.jpg'))
        except Exception as e:
            LOGGER.error(f"error remove {label}: {file}, {e}")
        return True
    return False


def check_and_save_target2(file, label, target_data_path, score=0.9226375818252563):
    label_path = os.path.join(target_data_path, label)
    os.makedirs(label_path, exist_ok=True)
    with open(file, 'r', encoding='utf-8') as f:
        content = json.load(f)
        f.close()
    shapes = content['shapes']
    if any(filter(lambda x: x['label'] == label and x['score'] == score, shapes)):
        LOGGER.info(f"find target label[{label}] in {file}")
        try:
            shutil.copyfile(file, os.path.join(label_path, os.path.basename(file)))
            shutil.copyfile(file.replace('.json', '.jpg'),
                            os.path.join(label_path, os.path.basename(file)).replace('.json', '.jpg'))
        except Exception as e:
            LOGGER.error(f"error backup {label}: {file}, {e}")
        return True
    return False


if __name__ == '__main__':
    # json_files = get_all_files(r'../../../data/forest_low_20240629/countdown')
    # json_files = get_all_files(r'../../../data/forest_new')
    # json_files = get_all_files(r'../../../data/forest_recheck_20240714')
    # target_data_path = r'../../../data/forest'
    target_data_path = r'Z:\disk2\脚本同步\forest\待标注数据\20240716'
    json_files = get_all_files(target_data_path)
    prevent_sleep()
    total_file = len(json_files)
    current = 0
    start = False
    for file in json_files:
        current += 1
        try:
            LOGGER.verbose(f"start file: {file}")
            check_and_save_target(file, 'gift', target_data_path)
            # check_and_save_target(file, 'sea_garbage', target_data_path)
            # check_and_save_target2(file, 'cooperation', target_data_path)
            # check_and_remvoe_target(file, 'magic_species')
            if current % 10 == 0:
                print(f"{current / total_file * 100:.2f}%")
        except Exception as e:
            LOGGER.error(f"error checking file: {file}, {e}")
            continue
    LOGGER.info(f"done. total file: {total_file} executed: {current}")
