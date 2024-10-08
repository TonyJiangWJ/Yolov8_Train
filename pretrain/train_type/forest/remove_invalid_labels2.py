import os
import json
import re
import shutil

from paddle_util.paddle_util import recognize_text
from lib.mylogger import LOGGER
from remove_invalid_labels import get_all_files, check_file_size_and_delete, check_collect_color, \
    check_file_content_and_remove_label, check_label_region, check_file_content_and_add_label, \
    check_file_and_remove_iou_labels
from train.win_power_control import prevent_sleep

if __name__ == '__main__':
    # json_files = get_all_files(r'../../../data/forest_low_20240629/countdown')
    # json_files = get_all_files(r'../../../data/forest_low_2_merge/gift')
    target_data_path = r'../../../data/forest_20240717/old_data'
    # target_data_path = r'Z:\disk2\脚本同步\forest\待标注数据\20240716'
    recheck_path = os.path.join(target_data_path, 'recheck')
    recheck_doubt_path = os.path.join(target_data_path, 'recheck_doubt')
    delete_path = os.path.join(target_data_path, 'delete')
    json_files = get_all_files(target_data_path)
    os.makedirs(recheck_path, exist_ok=True)
    os.makedirs(recheck_doubt_path, exist_ok=True)
    os.makedirs(delete_path, exist_ok=True)
    prevent_sleep()
    total_file = len(json_files)
    current = 0
    start = False
    for file in json_files:
        current += 1
        # if start is False:
        #     if file.__contains__('1708574786089648'):
        #         start = True
        #     else:
        #         continue
        # if os.path.exists(r"E:\Repository\Yolov8_Train\data\forest_20240713\1719494857012476.json"):
        #     file = r'E:\Repository\Yolov8_Train\data\forest_20240713\1719494857012476.json'
        try:
            LOGGER.verbose(f"start file: {file}")
            if check_file_size_and_delete(file, delete_path):
                continue
            changed = False
            doubt = False
            changed |= check_collect_color(file)
            changed |= check_file_content_and_remove_label(file, 'collect', ['one_key'])
            changed |= check_label_region(file, re.compile('还剩'), 'countdown', ['绿色', 'g'], 'cannot')
            changed |= check_label_region(file, re.compile('绿色|\\dg'), 'cannot', ['还剩'], 'countdown')
            c, d = check_file_content_and_add_label(file, ['collect', 'water'], {
                "label": "one_key",
                "score": None,
                "points": [
                    [
                        251.0344827586207,
                        800.080459770115
                    ],
                    [
                        390.1149425287356,
                        800.080459770115
                    ],
                    [
                        390.1149425287356,
                        846.0574712643679
                    ],
                    [
                        251.0344827586207,
                        846.0574712643679
                    ]
                ],
                "group_id": None,
                "description": "",
                "difficult": False,
                "shape_type": "rectangle",
                "flags": {},
                "attributes": {}
            }, ocr_check=re.compile('一?键收'))
            changed |= c
            doubt |= False if d is None else d
            c, d = check_file_content_and_add_label(file, ['energy_ocr'], {
                "label": "cooperation",
                "score": 0.404,
                "points": [
                    [
                        524.4311199188232,
                        668.4598543167115
                    ],
                    [
                        593.3743389129639,
                        668.4598543167115
                    ],
                    [
                        593.3743389129639,
                        708.2236055374145
                    ],
                    [
                        524.4311199188232,
                        708.2236055374145
                    ]
                ],
                "group_id": None,
                "description": None,
                "difficult": False,
                "shape_type": "rectangle",
                "flags": {},
                "attributes": {}
            }, ocr_check=re.compile('合种'))
            changed |= c
            doubt |= False if d is None else d
            # changed |= check_label_region(file, re.compile('合种'), 'cooperation', None, None)
            changed |= check_file_and_remove_iou_labels(file)
            if changed:
                # copy and recheck
                try:
                    shutil.copyfile(file, os.path.join(recheck_path, os.path.basename(file)))
                    shutil.copyfile(file.replace('.json', '.jpg'),
                                    os.path.join(recheck_path, os.path.basename(file)).replace('.json', '.jpg'))
                except Exception as e:
                    LOGGER.error(f"error backup recheck: {file}, {e}")
            if doubt:
                try:
                    shutil.copyfile(file, os.path.join(recheck_doubt_path, os.path.basename(file)))
                    shutil.copyfile(file.replace('.json', '.jpg'),
                                    os.path.join(recheck_doubt_path, os.path.basename(file)).replace('.json', '.jpg'))
                except Exception as e:
                    LOGGER.error(f"error backup doubt: {file}, {e}")
            if current % 10 == 0:
                print(f"{current / total_file * 100:.2f}%")
        except Exception as e:
            LOGGER.error(f"error checking file: {file}, {e}")
            continue
    LOGGER.info(f"done. total file: {total_file} executed: {current}")
