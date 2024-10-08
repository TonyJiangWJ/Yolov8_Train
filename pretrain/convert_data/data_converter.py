
import json
import shutil
from pathlib import Path
from ultralytics import YOLO
from convert_to_yolo_txt import ShapeInfo
import os
import cv2
from PIL import Image
import label_config
import numpy as np

COLOR_RED = '\033[0;31m'
COLOR_GREEN = '\033[0;32m'
COLOR_YELLOW = '\033[0;33m'
COLOR_RESET = '\033[0m'


# best_model = YOLO(model='config/best.pt')


def predict_and_save(img_path, predict_result_path):
    if not os.path.exists(img_path):
        print(f"{COLOR_RED}文件路径不存在：{img_path}{COLOR_RESET}")
        return
    img_path = os.path.normpath(img_path)
    # image = cv2.imread(img_path)
    image = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
    if image is None:
        print(f"{COLOR_RED}图片读取失败：{img_path}{COLOR_RESET}")
        return
    # 需要将文件保存到本地，否则webdav读取有些问题
    tmp_file_path = os.path.join(project_path, 'tmp.jpg')
    cv2.imwrite(tmp_file_path, image)
    # 指定project為當前執行目錄，否則會按settings文件中的地址進行保存
    result = best_model.predict(project=project_path, source=tmp_file_path, save=False)

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
            shape['score'] = float(confidence)
            width, height = (right - x), (bottom - y)
            if confidence > confidence_threshold:
                if area_threshold is not None and width * height < area_threshold:
                    print("%sinvalid for classId: %.0f confidence: %.2f x: %.2f y: %.2f w: %.2f h: %.2f"
                          " area too small %.2f %s" % (
                              COLOR_RED, classId, confidence, x, y, width, height, width * height, COLOR_RESET))
                    continue
                shapes.append(shape)
                print(str(predict_target))
                print("valid for classId: %.0f[%s] confidence: %.2f x: %.2f y: %.2f w: %.2f h: %.2f area: %.2f\n" % (
                    classId, label, confidence, x, y, width, height, width * height))
            else:
                print("%sinvalid for classId: %.0f confidence: %.2f x: %.2f y: %.2f w: %.2f h: %.2f %s" % (
                    COLOR_RED, classId, confidence, x, y, width, height, COLOR_RESET))
        if len(shapes) == 0:
            print(f"{COLOR_YELLOW}image has no reco shapes:{img_path}{COLOR_RESET}")
            img_file = predict_result_path + '/no_label/' + os.path.basename(img_path).replace('.data', '')
            shutil.copyfile(img_path, img_file)
            return
        predict_info['shapes'] = shapes

        predict_info['imagePath'] = os.path.basename(img_path).replace('.data', '')
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


def predict_and_save_for_path(image_path, predict_result_path):
    count = 0
    for root, dirs, file_list in os.walk(image_path):
        # print("dir:" + str(dirs))
        if root.__contains__('predict') or root.__contains__('no_label'):
            print("跳过predict文件夹")
            continue
        for file in file_list:
            if max_predict_num is not None and count >= max_predict_num:
                print(f"当前预测总数：{count}大于等于最大值{max_predict_num} 跳过处理")
                break
            if file.endswith("jpg") or file.endswith(".data"):
                if overwrite_predict_result is False:
                    predict_json_path = os.path.join(predict_result_path, file.replace('jpg', 'json').replace('jpg.data', 'json'))
                    if os.path.exists(predict_json_path):
                        print(f"predict result is exists skip it:{predict_json_path}")
                        continue
                operate_file = os.path.join(root, file)
                if overwrite_label or not os.path.exists(operate_file.replace('jpg', 'json').replace('jpg.data', 'json')):
                    try:
                        predict_and_save(operate_file, predict_result_path)
                    except Exception as e:
                        print("predict failed:" + operate_file)
                        print(e)
                        continue
                    count += 1
    print(f"已完成{count}张图片的预测")
    return count


def prepare_result_path(predict_save_path, sub_dir):
    predict_result_path = os.path.join(predict_save_path, sub_dir)
    # 先清空预测结果，然后重新创建目录
    removed = True
    if os.path.exists(predict_result_path):
        if overwrite_predict_result is False:
            removed = False
        else:
            try:
                print(f"正在删除{sub_dir}文件夹，请稍候：{predict_result_path}")
                shutil.rmtree(predict_result_path)
                print(f"删除{sub_dir}文件夹成功")
            except:
                removed = False
                print(f"删除{sub_dir}文件夹异常，可能使用中")
    else:
        removed = True
    if removed:
        os.makedirs(predict_result_path, exist_ok=True)
    return predict_result_path


def predict_images(image_path, target_dir):
    predict_result_path = prepare_result_path(target_dir, 'predict')
    prepare_result_path(target_dir, 'no_label')

    # 预测单张图片
    # predict_and_save("H:/Projects/repository/datasets/tiktok/20230903/169374856199190.jpg")
    return predict_and_save_for_path(image_path, predict_result_path)

# 直接在webdav之间读取和预测，保存预测后数据
if __name__ == '__main__':

    source_dir = r"W:/"
    target_dir = r"Z:\disk2\脚本同步\forest\待标注数据\20240716"
    total_predict = 0
    # 判定阈值，初始模型可以设置低一些 验证模型时设置一个较高值
    confidence_threshold = 0.5
    # 面积判定，低于此面积的判定为无效，设置为None则关闭
    area_threshold = None
    # 设置最大预测图片数, 不限制时设置为None
    max_predict_num = None
    # 是否覆盖原标签数据 即当前图片的json文件存在时 是否重新预测
    overwrite_label = True
    # 是否覆盖预测结果
    overwrite_predict_result = True
    # 标签列表
    labels = label_config.ant_forest
    # 项目地址，不配置的话会从首次运行的项目地址运行，导致非预期的结果
    project_path = os.path.join("../../train/runs")
    # 指定模型地址，进行模型初始化
    best_model = YOLO(model=os.path.join(r'../../train/runs/detect/train26/weights/best.pt'))
    # 待识别的图片地址
    # root_path = r"K:\YOLOV8_train_clean\data\yuanshen_stone\predict"
    # root_path = r"H:\Projects\repository\Coding\video_saving"
    root_path = source_dir
    total_predict += predict_images(root_path, target_dir)
    # 如果是有子目录的，使用如下方式
    # for path in os.listdir(root_path):
    #     total_predict += predict_images(os.path.join(root_path, path))
    # for path in ["关闭按钮成功"]:
    #     predict_images(os.path.join(root_path, path))
    print(f"总计处理图片：{total_predict}")

