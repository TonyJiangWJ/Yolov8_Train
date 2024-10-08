from ultralytics import YOLO
import os

from split import split_dataset
from posttrain.export_x_anylabeling_model import export_x_anylabeling_model_file
import label_config


def redo_split_dataset():
    # 数据集划分比例，训练集70%，验证集15%，测试集15%，按需修改
    train_percent = 0.7
    val_percent = 0.15
    test_percent = 0.15
    root_path = "../datasets"
    source_train_type = 'ad'
    split_dataset(train_percent, val_percent, test_percent, root_path, source_train_type)


##
# 从start_model开始，循环训练模型，每次训练前重新split拆分数据集 需要先执行convert_to_yolo_text.py将数据集转换为yolo格式
# 训练完成后，将模型转换为onnx 并生成x-anylabeling的yml配置文件 用于x-anylabeling的模型导入
##
if __name__ == '__main__':
    # Load a model
    # model = YOLO('yolov8n.pt')
    # model = YOLO('yolov8n.pt')
    loop_size = 5
    start_model = 22

    while loop_size > 0:
        redo_split_dataset()
        pre_train_model = os.path.abspath(rf'./runs/detect/train{start_model}/weights/best.pt')
        model = YOLO(pre_train_model)
        # Train the model
        results = model.train(data=os.path.abspath(r'../config/ad.yaml'), epochs=200, imgsz=480, device=0,
                              workers=32, batch=32,
                              patience=100)
        start_model += 1
        loop_size -= 1

    model_path = os.path.abspath(rf'./runs/detect/train{start_model}/weights/best.onnx')
    export_x_anylabeling_model_file(model_path, label_config.ad, 'ad', f'广告-{start_model}')
    print('done')