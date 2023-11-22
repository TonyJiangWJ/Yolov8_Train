import json
import shutil
from pathlib import Path
from ultralytics import YOLO
from convert_to_yolo_txt import ShapeInfo
import os
import cv2
from PIL import Image
import label_config

COLOR_RED = '\033[0;31m'
COLOR_GREEN = '\033[0;32m'
COLOR_YELLOW = '\033[0;33m'
COLOR_RESET = '\033[0m'
root_image_path = 'H:/Projects/repository/datasets/manor'
predict_result_path = os.path.join(root_image_path, 'predict')
if not os.path.exists(predict_result_path):
    os.mkdir(predict_result_path)
# best_model = YOLO(model='config/best.pt')

labels = label_config.manor


def predict_and_save(img_path):
    if not os.path.exists(img_path):
        print(f"{COLOR_RED}文件路径不存在：{img_path}{COLOR_RESET}")
        return
    # 指定project為當前執行目錄，否則會按settings文件中的地址進行保存
    result = best_model.predict(project="K:/YOLOV8_train_clean/runs", source=img_path, save=True)

    for depth1 in result:
        for depth2 in depth1:
            print(str(depth2))
            predict_target = depth2[0].boxes.data[0]
            x, y, right, bottom, confidence, classId = predict_target
            x = int(x)
            y = int(y)
            right = int(right)
            bottom = int(bottom)
            label = labels[int(classId)]
            if confidence > 0.5:
                print(str(predict_target))
                print("valid for classId: %.0f[%s] confidence: %.2f x: %.2f y: %.2f w: %.2f h: %.2f\n" % (
                    classId, label, confidence, x, y, right - x, bottom - y))
            else:
                print("%sinvalid for classId: %.0f confidence: %.2f x: %.2f y: %.2f w: %.2f h: %.2f %s" % (
                    COLOR_RED, classId, confidence, x, y, right - x, bottom - y, COLOR_RESET))



if __name__ == '__main__':
    best_model = YOLO(model='K:/YOLOV8_train_clean/runs/detect/manor_v4/weights/best.pt')
    # predict_and_save("K:/YOLOV8_train_clean/datasets/manor/train/images/16927420177525.jpg")
    root_path = "H:/Projects/repository/datasets/manor"
    file_list = os.listdir(root_path)
    for file in file_list:
        if file.endswith("jpg"):
            predict_and_save(os.path.join(root_path, file))
