import json
from pathlib import Path
from ultralytics import YOLO
from convert_to_yolo_txt import ShapeInfo

best_model = YOLO(model='K:/YOLOV8_train_clean/runs/detect/manor_v1/weights/best.pt')
# best_model = YOLO(model='config/best.pt')

# img_path = '1.jpg'
img_path = 'K:/YOLOV8_train_clean/datasets/manor/images/169275806845675.jpg'
# img_path = 'datasets/rebar/images/000208.jpg'

import os
import cv2
from PIL import Image
import label_config

COLOR_RED = '\033[0;31m'
COLOR_GREEN = '\033[0;32m'
COLOR_YELLOW = '\033[0;33m'
COLOR_RESET = '\033[0m'
image = cv2.imread(img_path)
# 指定project為當前執行目錄，否則會按settings文件中的地址進行保存
result = best_model.predict(project="K:/YOLOV8_train_clean/runs", source=img_path, save=True)

# 在图像上绘制文本
text = "Hello, OpenCV!"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (255, 255, 255)  # 白色
thickness = 2

# 绘制矩形
color = (0, 255, 0)  # 绿色


labels = label_config.manor
predict_info = {}
for depth1 in result:
    predict_info['imagePath'] = os.path.basename(img_path)
    predict_info['imageWidth'] = image.shape[0]
    predict_info['imageHeight'] = image.shape[1]
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
        if confidence > 0.5:
            print(str(predict_target))
            print("valid for classId: %.0f[%s] confidence: %.2f x: %.2f y: %.2f w: %.2f h: %.2f\n" % (
                classId, label, confidence, x, y, right - x, bottom - y))
            cv2.putText(image, "%s:%.2f" % (label, confidence), (int(x), int(y)), font, font_scale,
                        font_color, thickness)
            start_point = (int(x), int(y))
            end_point = (int(right), int(bottom))
            cv2.rectangle(image, start_point, end_point, color, thickness)
        else:
            print("%sinvalid for classId: %.0f confidence: %.2f x: %.2f y: %.2f w: %.2f h: %.2f %s" % (
                COLOR_RED, classId, confidence, x, y, right - x, bottom - y, COLOR_RESET))
    predict_info['shapes'] = shapes
    print(f"shapeInfo: {str(predict_info)}")
# print("predict result: %s" % str(result))
print("save path:" + str(best_model.predictor.save_dir / os.path.basename(img_path)))
# best_model.predictor.save_dir / os.path.basename(img_path)

cv2.imshow('Inference Result', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
