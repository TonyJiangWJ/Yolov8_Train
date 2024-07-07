from ultralytics import YOLO
import os
import yaml
import label_config


def export_onnx_if_not_exists():
    if not os.path.exists(model_path):
        raise FileExistsError('模型文件不存在')
    if os.path.exists(onnx_path):
        print("onnx 文件已存在")
        return
    # Load a model
    model = YOLO(model_path)
    model.export(format='onnx', opset=12)


# 创建anylabeling中使用的自定义模型，但是实际效果有点差 目前还是使用批量识别比较方便
if __name__ == '__main__':
    labels = label_config.tiktok
    project_path = "E:/Repository/YOLOV8_train/"
    model_path = f"{project_path}runs/detect/tiktok_v1.2/weights/best.pt"
    onnx_path = model_path.replace(".pt", ".onnx")
    yaml_path = model_path.replace(".pt", ".yaml")
    export_onnx_if_not_exists()
    # 定义模型数据
    yaml_data = {
        'type': 'yolov8',
        'name': 'tiktok',
        'display_name': 'tiktok',
        'model_path': onnx_path,
        'confidence_threshold': 0.45,
        'input_height': 1024,
        'input_width': 1024,
        'nms_threshold': 0.45,
        'score_threshold': 0.5,
        'classes': label_config.to_list(labels)
    }
    # 使用PyYAML将数据写入YAML文件
    with open(yaml_path, 'w') as file:
        yaml.dump(yaml_data, file)
        file.close()
        print('anylabeling 自定义模型配置文件已保存到：', yaml_path)
