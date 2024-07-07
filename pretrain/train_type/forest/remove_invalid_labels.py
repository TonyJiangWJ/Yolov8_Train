import os
import json
import re
from paddle_util.paddle_util import recognize_text
from lib.mylogger import LOGGER



def get_all_files(root_dir):
    files = []
    for root, dirs, file in os.walk(root_dir):
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
        return

    new_shapes = [shape for shape in shapes if shape['label'] not in labels]
    if len(new_shapes) != len(shapes):
        LOGGER.info(f"changed file: {file}")
        content['shapes'] = new_shapes
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)
            f.close()


def check_file_and_remove_iou_labels(file):
    with open(file, 'r', encoding='utf-8') as f:
        content = json.load(f)
        f.close()
    shapes = content['shapes']
    # 计算iou 移除重叠的标注
    removed = False
    for shape in shapes:
        for shape2 in shapes:
            if shape == shape2:
                continue
            if shape['label'] == shape2['label']:
                continue
            if len(shape['points']) == 4:
                x1 = max(shape['points'][0][0], shape2['points'][0][0])
                y1 = max(shape['points'][0][1], shape2['points'][0][1])
                x2 = min(shape['points'][2][0], shape2['points'][2][0])
                y2 = min(shape['points'][2][1], shape2['points'][2][1])
            else:
                x1 = max(shape['points'][0][0], shape2['points'][0][0])
                y1 = max(shape['points'][0][1], shape2['points'][0][1])
                x2 = min(shape['points'][1][0], shape2['points'][1][0])
                y2 = min(shape['points'][1][1], shape2['points'][1][1])
            w = max(0, x2 - x1 + 1)
            h = max(0, y2 - y1 + 1)
            inter = w * h
            if len(shape['points']) == 4:
                area1 = (shape['points'][2][0] - shape['points'][0][0] + 1) * (
                        shape['points'][2][1] - shape['points'][0][1] + 1)
                area2 = (shape2['points'][2][0] - shape2['points'][0][0] + 1) * (
                        shape2['points'][2][1] - shape2['points'][0][1] + 1)
            else:
                area1 = (shape['points'][1][0] - shape['points'][0][0] + 1) * (
                        shape['points'][1][1] - shape['points'][0][1] + 1)
                area2 = (shape2['points'][1][0] - shape2['points'][0][0] + 1) * (
                        shape2['points'][1][1] - shape2['points'][0][1] + 1)
            iou = inter / (area1 + area2 - inter)
            if iou > 0.7:
                removed = True
                LOGGER.verbose(
                    f"{file} iou: {iou} 重叠标注：{shape['label']}[{shape['score']}] {shape2['label']}[{shape2['score']}]")
                if shape['score'] > shape2['score']:
                    LOGGER.info(f"remove {shape2['label']}")
                    shapes.remove(shape2)
                else:
                    shapes.remove(shape)
                    LOGGER.info(f"remove {shape['label']}")
                break

    if removed:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)
            f.close()


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


if __name__ == '__main__':
    # json_files = get_all_files(r'../../../data/forest_low_20240629/countdown')
    # json_files = get_all_files(r'../../../data/forest_new')
    json_files = get_all_files(r'../../../data/forest_low_2_merge')
    for file in json_files:
        check_file_content_and_remove_label(file, 'collect', ['one_key'])
        check_file_and_remove_iou_labels(file)
        check_label_region(file, re.compile('还剩'), 'countdown', ['绿色', 'g'], 'cannot')
        check_label_region(file, re.compile('绿色|\\dg'), 'cannot', ['还剩'], 'countdown')
        check_label_region(file, re.compile('一?键收'), 'one_key', None, None)
