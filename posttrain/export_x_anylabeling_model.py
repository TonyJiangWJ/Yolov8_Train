import label_config
import yaml
import os
from posttrain.opt_onnx_model import export_onnx_and_opt


def export_x_anylabeling_model_file(model_path, classes, name, display_name, nms_threshold=0.45,
                                    confidence_threshold=0.3):
    type = 'yolov8'
    # name = 'ant-forest'
    # 必须是onnx模型
    # model_path = '../train/runs/detect/train40/weights/best.onnx'
    # classes = label_config.ant_forest

    # classes 从键值对转换成数组
    classes = list(classes.values())

    if not model_path.endswith('.onnx'):
        raise ValueError('模型文件必须是onnx格式')

    model_path = os.path.abspath(model_path)
    print('model_path:', model_path)
    if os.path.exists(model_path) is False:
        export_onnx_and_opt(model_path.replace('.onnx', '.pt'))
    target_path = model_path.replace('.onnx', '.yaml')

    # 将上述字段导出成yaml文件到target_path

    data = {
        'type': type,
        'display_name': display_name,
        'nms_threshold': nms_threshold,
        'confidence_threshold': confidence_threshold,
        'name': name,
        'model_path': model_path,
        'classes': classes
    }
    with open(target_path, 'w', encoding='utf-8') as f:
        # yaml.dump时对中文内容进行额外处理
        yaml.dump(data, f, allow_unicode=True, encoding='utf-8')
        f.close()


if __name__ == '__main__':
    export_x_anylabeling_model_file('../train/results/manor/best.onnx', label_config.manor,
                                    'manor',
                                    display_name='蚂蚁庄园v1')
