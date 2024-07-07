import os
import json


def get_all_files(root_dir):
    files = []
    for root, dirs, file in os.walk(root_dir):
        for f in file:
            # 是否以.json结尾
            if f.endswith('.json'):
                files.append(os.path.join(root, f))
    return files


def check_file_content_and_inject_label(file, labelInfo):
    with open(file, 'r', encoding='utf-8') as f:
        content = json.load(f)
        f.close()
    shapes = content['shapes']

    # 使用lambda方式判断shapes中是否存在label=energy_ocr的值，赋值给一个变量
    has_ocr_label = any(filter(lambda x: x['label'] == 'cooperation', shapes))
    if has_ocr_label is True:
        return

    injected = False
    # 判断shapes中是否存在label='backpack'，如果存在，则在shapes中加入labelInfo
    for shape in shapes:
        if shape['label'] == 'magic_species':
            shapes.append(labelInfo)
            injected = True
            break
    if injected is True:
        print(f"injected into file: {file}")
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)
            f.close()


if __name__ == '__main__':
    json_files = get_all_files(r'..\..\..\data\forest_20240705\home')
    for file in json_files:
        check_file_content_and_inject_label(file, {
            "label": "cooperation",
            "score": 0.6733019948005676,
            "points": [
                [
                    522.8965290069581,
                    661.0428005218506
                ],
                [
                    592.9022718429566,
                    661.0428005218506
                ],
                [
                    592.9022718429566,
                    709.9960607528686
                ],
                [
                    522.8965290069581,
                    709.9960607528686
                ]
            ],
            "description": "",
            "shape_type": "rectangle",
            "flags": {},
            "attributes": {}
        })
