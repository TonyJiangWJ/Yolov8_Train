import json
import shutil
from pathlib import Path
from typing import Sequence

import numpy
from cv2.typing import Size, Rect, Point
from ultralytics import YOLO
from convert_to_yolo_txt import ShapeInfo
import os
import cv2
from PIL import Image, ImageDraw, ImageFont
import label_config

COLOR_RED = '\033[0;31m'
COLOR_GREEN = '\033[0;32m'
COLOR_YELLOW = '\033[0;33m'
COLOR_RESET = '\033[0m'


# best_model = YOLO(model='config/best.pt')
def cv2_img_add_ch_text(img, text, left, top, text_color=(0, 255, 0), text_size=20):
    # 判断是否OpenCV图片类型
    if isinstance(img, numpy.ndarray):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    font_text = ImageFont.truetype("msyh.ttc", text_size, encoding="utf-8")
    draw.text((left, top - text_size - 5), text, text_color, font=font_text)
    return cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)


def convert(image, ori_position):
    h, w = image.shape[0], image.shape[1]
    ratio = h / 1440
    return int(ori_position[0] * ratio), int(ori_position[1] * ratio)


def predict_and_draw(image, frame_num):
    # 指定project為當前執行目錄，否則會按settings文件中的地址進行保存
    result = best_model.predict(project=project_path, source=image, save=False)
    # uid添加遮罩
    cv2.rectangle(image, convert(image, (2240, 1400)), convert(image, (2500, 1440)), color=(88, 88, 88),
                  thickness=cv2.FILLED)
    predict_info = {}
    for depth1 in result:
        predict_info['version'] = '0.3.3'
        predict_info['flags'] = {}
        shapes = []
        for depth2 in depth1:
            # print(str(depth2))
            predict_target = depth2[0].boxes.data[0]
            x, y, right, bottom, confidence, classId = predict_target
            x = int(x)
            y = int(y)
            right = int(right)
            bottom = int(bottom)
            shape = {}
            label = labels[int(classId)]
            shape['label'] = label
            shape['text'] = ''
            shape['group_id'] = None
            shape['shape_type'] = 'rectangle'
            shape['points'] = [
                [x, y],
                [right, bottom]
            ]
            width, height = (right - x), (bottom - y)
            if confidence > confidence_threshold:
                if area_threshold is not None and width * height < area_threshold:
                    print("%sinvalid for classId: %.0f confidence: %.2f x: %.2f y: %.2f w: %.2f h: %.2f"
                          " area too small %.2f %s" % (
                              COLOR_RED, classId, confidence, x, y, width, height, width * height, COLOR_RESET))
                    continue
                # 在帧上绘制矩形框
                cv2.rectangle(image, (x, y), (right, bottom), (0, 255, 0), 2)
                # 在帧上添加文字
                image = cv2_img_add_ch_text(image, f"{label}:{confidence:.2}", x, y, (0, 255, 0), 20)
                shapes.append(shape)
                print(str(predict_target))
                print("valid for classId: %.0f[%s] confidence: %.2f x: %.2f y: %.2f w: %.2f h: %.2f area: %.2f\n" % (
                    classId, label, confidence, x, y, width, height, width * height))
            else:
                print("%sinvalid for classId: %.0f confidence: %.2f x: %.2f y: %.2f w: %.2f h: %.2f %s" % (
                    COLOR_RED, classId, confidence, x, y, width, height, COLOR_RESET))
        if len(shapes) == 0:
            print(f"{COLOR_YELLOW}image has no reco shapes:{frame_num}{COLOR_RESET}")
            return image
        predict_info['shapes'] = shapes

        predict_info['imagePath'] = None
        predict_info['imageData'] = None
        predict_info['imageWidth'] = image.shape[1]
        predict_info['imageHeight'] = image.shape[0]
        predict_info['text'] = ""
        print(f"shapeInfo: {str(predict_info)}")
    return image


def predict_video(video_path, target_path):
    video = cv2.VideoCapture(video_path)

    # 获取视频的帧率和分辨率
    fps = int(video.get(cv2.CAP_PROP_FPS))
    target_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    target_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # 设置保存修改后视频的编解码器和输出，指定路径，格式，帧率，图像大小
    out = cv2.VideoWriter(target_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (target_width, target_height))

    # 指定帧范围，全量的话设置为空数组即可
    predict_frame_range = []
    frame_num = 0
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        frame_num += 1
        print(f'current frame: {frame_num}')
        if predict_frame_range is not None and len(predict_frame_range) == 2:
            if frame_num < predict_frame_range[0]:
                continue
            elif frame_num > predict_frame_range[1]:
                break
        out.write(predict_and_draw(frame, frame_num))

    print(f'done video frames: {frame_num} output path: {target_path}')
    video.release()


if __name__ == '__main__':
    # 判定阈值，初始模型可以设置低一些 验证模型时设置一个较高值
    confidence_threshold = 0.7
    # 面积判定，低于此面积的判定为无效，设置为None则关闭
    area_threshold = None
    # 标签列表
    labels = label_config.yuanshen_chz
    # 项目地址，不配置的话会从首次运行的项目地址运行，导致非预期的结果
    project_path = "K:/YOLOV8_train_clean/runs"
    # 指定模型地址，进行模型初始化
    best_model = YOLO(model='K:/YOLOV8_train_clean/train/runs/detect/train14/weights/best.pt')
    # predict_video('F:/NVIDIA_RECORD/VIDEOS/Yuan Shen 原神/find_entry_fire.mp4',
    #               'F:/NVIDIA_RECORD/VIDEOS/Yuan Shen 原神/predicted_find_entry_fire.mp4')
    root_path = r'F:\NVIDIA_RECORD\VIDEOS\Yuan Shen 原神\20230922'
    if not os.path.exists(root_path + '/predict'):
        os.mkdir(root_path + '/predict')
    for file in os.listdir(root_path):
        if not file.endswith('.mp4'):
            continue
        predict_file_name = file.replace(".mp4", "_predict.mp4")
        predict_video(os.path.join(root_path, file), os.path.join(root_path, 'predict', predict_file_name))
    # predict_video('F:/NVIDIA_RECORD/VIDEOS/Yuan Shen 原神/Yuan Shen 原神 2023.09.16 - 00.31.58.01.mp4',
    #               'F:/NVIDIA_RECORD/VIDEOS/Yuan Shen 原神/predicted_0917-秘境4.mp4')
