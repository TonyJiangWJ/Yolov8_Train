import os
import json
import re
import shutil

import cv2
import numpy as np

from paddle_util.paddle_util import recognize_text
from lib.mylogger import LOGGER
from lib.opencv_helper import get_hist_avg
from train.win_power_control import allow_sleep, prevent_sleep


def get_all_files(root_dir):
    files = []
    for root, dirs, file in os.walk(root_dir):
        if root.__contains__(r'\recheck') or root.__contains__(r'\recheck_doubt') or root.__contains__(
                r'\delete') or root.__contains__(r'\gift'):
            print(f"跳过文件夹：{root}")
            continue
        for f in file:
            # 是否以.json结尾
            if f.endswith('.json'):
                json_file = os.path.join(root, f)
                if os.path.exists(json_file.replace('.json', '.jpg')) is False:
                    LOGGER.error(f"jpg file is not exist: {json_file.replace('.json', '.jpg')}")
                    os.remove(json_file)
                else:
                    files.append(os.path.join(root, f))
    return files


def check_file_content_and_remove_label(file, exclude_label, labels):
    with open(file, 'r', encoding='utf-8') as f:
        content = json.load(f)
        f.close()
    shapes = content['shapes']

    # 使用lambda方式判断shapes中是否存在label=exclude_label的值，赋值给一个变量
    has_exclude_label = any(filter(lambda x: x['label'] == exclude_label, shapes))
    if has_exclude_label is True:
        return False

    new_shapes = [shape for shape in shapes if shape['label'] not in labels]
    if len(new_shapes) != len(shapes):
        LOGGER.info(f"changed file: {file}")
        content['shapes'] = new_shapes
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)
            f.close()
        return True
    return False


def check_file_content_and_add_label(file, include_labels, shapeInfo, ocr_check) -> (bool, bool):
    with open(file, 'r', encoding='utf-8') as f:
        content = json.load(f)
        f.close()
    shapes = content['shapes']

    # 使用lambda方式判断shapes中是否同时存在include_labels中包含的标签
    has_include_label = True
    for include_label in include_labels:
        has_include_label &= any(filter(lambda x: x['label'] == include_label, shapes))
    has_target_label = any(filter(lambda x: x['label'] == shapeInfo['label'], shapes))
    # print(f"has_target_label [{shapeInfo['label']}]：{has_target_label}")
    if has_target_label is True or has_include_label is False:
        return False, False

    if ocr_check is not None:
        points = shapeInfo['points']
        if len(points) == 4:
            x1, y1 = points[0]
            x2, y2 = points[2]
        else:
            x1, y1 = points[0]
            x2, y2 = points[1]
        reco_text = recognize_text(file.replace('.json', '.jpg'), [x1, y1, x2, y2])
        if ocr_check.search(reco_text) is None:
            LOGGER.warn(f"can not recognize target text: {ocr_check} => [{reco_text}] will not add label {file}")
            return False, True
    LOGGER.info(f"changed file: {file} added: {shapeInfo['label']}")
    shapes.append(shapeInfo)
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)
        f.close()
    return True, False


def getXYInfo(points):
    if len(points) == 4:
        x1, y1 = points[0]
        x2, y2 = points[2]
    else:
        x1, y1 = points[0]
        x2, y2 = points[1]
    return x1, y1, x2, y2


def check_file_and_remove_iou_labels(file):
    with open(file, 'r', encoding='utf-8') as f:
        content = json.load(f)
        f.close()
    shapes = content['shapes']
    # 计算iou 移除重叠的标注
    removed = False
    removedIdx = []
    for index, shape in enumerate(shapes):
        if index in removedIdx:
            continue
        for index2, shape2 in enumerate(shapes):
            if index2 in removedIdx:
                continue
            if index == index2:
                continue
            # if shape['label'] == shape2['label']:
            #     continue
            # LOGGER.info(f"check file {file}")
            shapeXY1 = getXYInfo(shape['points'])
            # LOGGER.info(f"shape1: {shapeXY1}")
            shapeXY2 = getXYInfo(shape2['points'])
            # LOGGER.info(f"shape2: {shapeXY2}")
            x1 = max(shapeXY1[0], shapeXY2[0])
            y1 = max(shapeXY1[1], shapeXY2[1])
            x2 = min(shapeXY1[2], shapeXY2[2])
            y2 = min(shapeXY1[3], shapeXY2[3])
            w = max(0, x2 - x1 + 1)
            h = max(0, y2 - y1 + 1)
            inter = w * h
            ## (x2-x1) * (y2-y1)
            area1 = (shapeXY1[2] - shapeXY1[0] + 1) * (shapeXY1[3] - shapeXY1[1] + 1)
            area2 = (shapeXY2[2] - shapeXY2[0] + 1) * (shapeXY2[3] - shapeXY2[1] + 1)
            # LOGGER.info(f"area1: {area1} area2: {area2}")
            iou = inter / (area1 + area2 - inter)
            # LOGGER.verbose(f"inter: {inter} iou: {iou}")
            if iou > 0.7:
                removed = True
                # 以无分数的为优先 手动标注的是没有分数的
                if 'score' not in shape or shape['score'] is None:
                    shape['score'] = 1
                if 'score' not in shape2 or shape2['score'] is None:
                    shape2['score'] = 1

                LOGGER.verbose(
                    f"{file} iou: {iou} 重叠标注：{shape['label']}[{shape['score']}] {shape2['label']}[{shape2['score']}]")
                if shape['score'] > shape2['score']:
                    LOGGER.info(f"remove {shape2['label']}")
                    # shapes.remove(shape2)
                    removedIdx.append(index2)
                else:
                    # shapes.remove(shape)
                    LOGGER.info(f"remove {shape['label']}")
                    removedIdx.append(index)
                break

    if removed:
        new_shapes = []
        for index, shape in enumerate(shapes):
            if index not in removedIdx:
                new_shapes.append(shape)
        content['shapes'] = new_shapes
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)
            f.close()
        return True
    return False


def check_label_region(file, text, label, replace_text, replace_label):
    with open(file, 'r', encoding='utf-8') as f:
        content = json.load(f)
        f.close()
    shapes = content['shapes']
    replaced = False
    # 查找label匹配的shape列表
    target_labels = [shape for shape in shapes if shape['label'] == label]
    for shape in target_labels:
        points = shape['points']
        if len(points) == 4:
            x1, y1 = points[0]
            x2, y2 = points[2]
        else:
            x1, y1 = points[0]
            x2, y2 = points[1]
        reco_text = recognize_text(file.replace('.json', '.jpg'), [x1, y1, x2, y2])
        if text.search(reco_text) is None:
            LOGGER.warn(f"{file} this label is not valid: {shape['label']} reco text: {reco_text}")
            if replace_text is None:
                if reco_text == '':
                    LOGGER.info(f"{file} remove label {label}")
                    replaced = True
                    shapes.remove(shape)
            elif any(filter(lambda x: reco_text.__contains__(x), replace_text)):
                replaced = True
                shape['label'] = replace_label
                LOGGER.info(f"{file} change label from {label} to {replace_label}")
    if replaced:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)
            f.close()
        return True
    return False


def check_collect_color(file):
    with open(file, 'r', encoding='utf-8') as f:
        content = json.load(f)
        f.close()
    shapes = content['shapes']
    replaced = False
    # 查找label匹配的shape列表
    collect_labels = [shape for shape in shapes if shape['label'] == 'collect']
    cannot_labels = [shape for shape in shapes if shape['label'] == 'cannot']
    image = cv2.imdecode(np.fromfile(file.replace('.json', '.jpg'), dtype=np.uint8), -1)
    for shape in collect_labels:
        points = shape['points']
        if len(points) == 4:
            x1, y1 = points[0]
            x2, y2 = points[2]
        else:
            x1, y1 = points[0]
            x2, y2 = points[1]
        hist_avg = get_hist_avg(image, [x1,y1,x2,y2])
        if hist_avg < 25:
            LOGGER.warn(f"{file} label collect {x1,y1,x2,y2} is not valid hist: {hist_avg}")
            LOGGER.info(f"change label to cannot")
            shape['label'] = 'cannot'
            replaced = True
    for shape in cannot_labels:
        points = shape['points']
        if len(points) == 4:
            x1, y1 = points[0]
            x2, y2 = points[2]
        else:
            x1, y1 = points[0]
            x2, y2 = points[1]
        hist_avg = get_hist_avg(image, [x1,y1,x2,y2])
        if hist_avg >= 25:
            LOGGER.warn(f"{file} label cannot {x1,y1,x2,y2} is not valid hist: {hist_avg}")
            LOGGER.info(f"change label to collect")
            shape['label'] = 'collect'
            replaced = True
    if replaced:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)
            f.close()
        return True
    return False


def check_file_size_and_delete(file, delete_path):
    with open(file, 'r', encoding='utf-8') as f:
        content = json.load(f)
        f.close()
    imageWidth = content['imageWidth']
    imageHeight = content['imageHeight']
    if imageWidth > imageHeight:
        LOGGER.info(f"this file size is invalid: {file} w: {imageWidth} h: {imageHeight}")
        try:
            shutil.move(file, os.path.join(delete_path, os.path.basename(file)))
            shutil.move(file.replace('.json', '.jpg'),
                        os.path.join(delete_path, os.path.basename(file)).replace('.json', '.jpg'))
        except Exception as e:
            LOGGER.error(f"error backup delete: {file}, {e}")
        return True
    return False


def check_and_save_target(file, label, target_data_path):
    label_path = os.path.join(target_data_path, label)
    os.makedirs(label_path, exist_ok=True)
    with open(file, 'r', encoding='utf-8') as f:
        content = json.load(f)
        f.close()
    shapes = content['shapes']
    if any(filter(lambda x: x['label'] == label, shapes)):
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
    target_data_path = r'../../../data/forest_low_2_merge'
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
                "score": 0.9226375818252563,
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
            check_and_save_target(file, 'gift', target_data_path)
            if current % 10 == 0:
                print(f"{current / total_file * 100:.2f}%")
        except Exception as e:
            LOGGER.error(f"error checking file: {file}, {e}")
            continue
    LOGGER.info(f"done. total file: {total_file} executed: {current}")
