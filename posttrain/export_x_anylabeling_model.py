import label_config
import yaml

type = 'yolov8'
display_name = '蚂蚁庄园'
nms_threshold = 0.45
confidence_threshold = 0.3
name = 'manor'
# 必须是onnx模型
model_path = 'train/runs/detect/train11/weights/best.onnx'
classes = label_config.manor

# classes 从键值对转换成数组
classes = list(classes.values())

if not model_path.endswith('.onnx'):
    raise ValueError('模型文件必须是onnx格式')

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
with open(target_path, 'w') as f:
    # yaml.dump时对中文内容进行额外处理
    yaml.dump(data, f, allow_unicode=True)
    f.close()
