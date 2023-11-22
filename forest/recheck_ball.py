import os
import shutil

import cv2
import numpy as np
import json


def demo():
    # 读取图像
    img = cv2.imread('K:/YOLOV8_train_clean/datasets/forest/test/images/16931781847396.jpg')

    # 指定区域 [x, y, w, h]
    x = 169
    y = 334
    height = 441 - 334
    width = 261 - 169

    # 裁剪图像
    # 169, 334], [261, 441
    cropped_image = img[y:y + height, x:x + width]

    # 将裁剪后的图像从BGR颜色空间转换为RGB颜色空间
    cropped_image_rgb = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)

    # 计算H通道的直方图
    hist = cv2.calcHist([cropped_image_rgb], [0], None, [180], [0, 180])

    # 找到主要颜色的索引
    main_color_index = np.argmax(hist)

    print("main color:", main_color_index)


def get_main_hsv(image_path, x, y, width, height):
    img = cv2.imread(image_path)
    cropped_image = img[y:y + height, x:x + width]

    # cropped_image = cv2.threshold(cropped_image, 178, 255, cv2.THRESH_BINARY)
    # 将裁剪后的图像从BGR颜色空间转换为RGB颜色空间
    cropped_image_rgb = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)

    # 计算H通道的直方图
    hist = cv2.calcHist([cropped_image_rgb], [0], None, [180], [0, 180])

    # 找到主要颜色的索引
    main_color_index = np.argmax(hist)
    return main_color_index


def load_json(json_path):
    with open(json_path, 'r') as f:
        json_data = json.load(f)
        print(str(json_data['shapes']))
        shapes = json_data['shapes']
        image_path = json_data['imagePath']
        print(f"image_path: {image_path}")
        print(f"shapes: {shapes}")
        for shape in shapes:
            label = shape['label']
            points = shape['points']
            x = points[0][0]
            y = points[0][1]
            right = points[1][0]
            bottom = points[1][1]
            width = right - x
            height = bottom - y
            print(f"main color for {label} is {get_main_hsv(json_path.replace('json', 'jpg'), x, y, width, height)}")


def hex_to_rgb(hex_color):
    # 剥离 "#" 符号
    hex_color = hex_color.lstrip("#")

    # 将R、G和B的16进制值分别提取出来
    r_hex = hex_color[0:2]
    g_hex = hex_color[2:4]
    b_hex = hex_color[4:6]

    # 将16进制转换为十进制
    r = int(r_hex, 16)
    g = int(g_hex, 16)
    b = int(b_hex, 16)

    # 打印RGB值
    return r, g, b


def interval_image(image_path):
    image = cv2.imread(image_path)  # 0表示以灰度模式读取图像
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # 指定两个颜色范围
    lower_color = np.array(hex_to_rgb('#9bda00'), dtype=np.uint8)  # 较暗的蓝色
    upper_color = np.array(hex_to_rgb('#e1ff2f'), dtype=np.uint8)  # 较亮的蓝色

    # 使用inRange函数生成二值化图像
    return cv2.inRange(image, lower_color, upper_color)


def check_color_correct(image_path):
    print(f'check for {image_path}')
    json_path = image_path.replace('jpg', 'json')
    with open(json_path, 'r') as f:
        json_data = json.load(f)
        print(str(json_data['shapes']))
        shapes = json_data['shapes']
        # image_path = json_data['imagePath']
        print(f"image_path: {image_path}")
        print(f"shapes: {shapes}")
        image = interval_image(image_path)
        for shape in shapes:
            label = shape['label']
            if label == 'collect':
                points = shape['points']
                x = points[0][0]
                y = points[0][1]
                right = points[1][0]
                bottom = points[1][1]
                width = right - x
                height = bottom - y
                ball_region = image[y:y + height, x:x + width]
                count = cv2.countNonZero(ball_region)
                print(f'{label} ball count area: {count}')
                if count < 1000:
                    return False
                if y > 750:
                    return False
        f.close()
    return True


def check_predict_files(image_path, limit=None):
    file_list = os.listdir(image_path)
    incorrect_path = os.path.join(image_path,'incorrect')
    if os.path.exists(incorrect_path) is not True:
        os.mkdir(incorrect_path)
    count = 0
    for file in file_list:
        print(f'current: {count}')
        if file.endswith("jpg"):
            if check_color_correct(os.path.join(image_path, file)) is False:
                print(f'{os.path.join(image_path, file)}\'s predict info is incorrect')
                shutil.move(os.path.join(image_path, file), os.path.join(incorrect_path, file))
                json_file = file.replace('jpg', 'json')
                shutil.move(os.path.join(image_path, json_file), os.path.join(incorrect_path, json_file))
        count += 1
        if limit is not None and count >= limit:
            break
    print(f"已完成{count}张图片的检测")
    return count


if __name__ == "__main__":
    check_predict_files('H:/Projects/repository/datasets/ant_forest/merge202308-10/predict/', None)
    # load_json(r'H:/Projects/repository/datasets/ant_forest/merge202308-10/predict/1693298672866732.json')
    # check_color_correct('H:/Projects/repository/datasets/ant_forest/merge202308-10/predict/1693298672866732.jpg')
    #
    # cv2.imshow('Binary Image', interval_image('H:/Projects/repository/datasets/ant_forest/merge202308-10/predict/1693298672866732.jpg'))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
