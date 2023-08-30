import json
import shutil
from pathlib import Path
from ultralytics import YOLO
from convert_xml2json import ShapeInfo
import os
import cv2
from PIL import Image

COLOR_RED = '\033[0;31m'
COLOR_GREEN = '\033[0;32m'
COLOR_YELLOW = '\033[0;33m'
COLOR_RESET = '\033[0m'
# best_model = YOLO(model='config/best.pt')



def predict_and_save(img_path):
    if not os.path.exists(img_path):
        print(f"{COLOR_RED}文件路径不存在：{img_path}{COLOR_RESET}")
        return
    image = cv2.imread(img_path)
    # 指定project為當前執行目錄，否則會按settings文件中的地址進行保存
    result = best_model.predict(project="K:/YOLOV8_train_clean/runs", source=img_path, save=False)

    predict_info = {}
    for depth1 in result:
        predict_info['version'] = '0.3.3'
        predict_info['flags'] = {}
        shapes = []
        for depth2 in depth1:
            print(str(depth2))
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
            shapes.append(shape)
            if confidence > 0.15:
                print(str(predict_target))
                print("valid for classId: %.0f[%s] confidence: %.2f x: %.2f y: %.2f w: %.2f h: %.2f\n" % (
                    classId, label, confidence, x, y, right - x, bottom - y))
            else:
                print("%sinvalid for classId: %.0f confidence: %.2f x: %.2f y: %.2f w: %.2f h: %.2f %s" % (
                    COLOR_RED, classId, confidence, x, y, right - x, bottom - y, COLOR_RESET))
        predict_info['shapes'] = shapes

        predict_info['imagePath'] = os.path.basename(img_path)
        predict_info['imageData'] = None
        predict_info['imageWidth'] = image.shape[1]
        predict_info['imageHeight'] = image.shape[0]
        predict_info['text'] = ""
        print(f"shapeInfo: {str(predict_info)}")
        json_file = predict_result_path + '/' + predict_info['imagePath'].replace('jpg', 'json')
        img_file = predict_result_path + '/' + predict_info['imagePath']
        with open(json_file, 'w') as fw:
            json.dump(predict_info, fw)
            fw.close()
            print(f"已保存预测标注数据到：{json_file}")
            shutil.copyfile(img_path, img_file)


if __name__ == '__main__':
    # 标签列表
    labels = {
        0: "feed",
    }
    best_model = YOLO(model='K:/YOLOV8_train_clean/runs/detect/feed_v2/weights/last.pt')
    # predict_and_save("K:/YOLOV8_train_clean/datasets/manor/train/images/16927420177525.jpg")
    root_path = "H:/Projects/repository/datasets/feed"
    root_image_path = 'H:/Projects/repository/datasets/feed'
    predict_result_path = os.path.join(root_image_path, 'predict')
    if not os.path.exists(predict_result_path):
        os.mkdir(predict_result_path)
    file_list = os.listdir(root_path)
    for file in file_list:
        if file.endswith("jpg"):
            if not os.path.exists(root_path + '/' + file.replace('jpg', 'json')):
                predict_and_save(os.path.join(root_path, file))
