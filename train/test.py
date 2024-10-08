from ultralytics import YOLO
import os

from split import split_dataset
from posttrain.export_x_anylabeling_model import export_x_anylabeling_model_file
import label_config
if __name__ == '__main__':

    start_model = 31
    model_path = os.path.abspath(rf'./runs/detect/train{start_model}/weights/best.onnx')
    export_x_anylabeling_model_file(model_path, label_config.ad, 'ad', f'广告-{start_model}')