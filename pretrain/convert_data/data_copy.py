
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

def copy_images(source_path, target_path, limit=100):
    total = 0
    for file in os.listdir(source_path):
        print(f"read file/dir: {file} {os.path.join(source_path, file)}")
        if file.__contains__('manor'):
            print('skip manor files')
            continue
        if os.path.isdir(os.path.join(source_path, file)):
            print(f"dir: {file}")
            # 文件夹 不存在时创建
            if os.path.exists(os.path.join(target_path, file)) is False:
                print(f"create dir: {(os.path.join(target_path, file))}")
                os.mkdir(os.path.join(target_path, file))
            # 复制子目录文件
            total += copy_images(os.path.join(source_path, file), os.path.join(target_path, file), limit)
        else:
            print(f"file: {file}")
            if file.endswith('.data'):
                shutil.copyfile(os.path.join(source_path, file), os.path.join(target_path, file.replace('.data', '')))
            else:
                shutil.copyfile(os.path.join(source_path, file), os.path.join(target_path, file))
            total += 1
            if limit is not None and total > limit:
                return total
    return total



# 直接从webdav复制图片
if __name__ == '__main__':

    source_dir = r"Z:\disk2\脚本同步\小鸡\待标注数据\20240920"
    target_dir = r"F:\datasets\manor\20240920"
    if os.path.exists(target_dir) is False:
        os.makedirs(target_dir)
    total_copied = 0
    root_path = source_dir
    total_copied += copy_images(root_path, target_dir, limit=100)
    # 如果是有子目录的，使用如下方式
    # for path in os.listdir(root_path):
    #     total_predict += predict_images(os.path.join(root_path, path))
    # for path in ["关闭按钮成功"]:
    #     predict_images(os.path.join(root_path, path))
    print(f"总计处理图片：{total_copied}")

