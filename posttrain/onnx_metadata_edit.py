import onnx
import json

# 加载现有的 ONNX 模型
model_path = '../train/runs/detect/train13/weights/best_lite.onnx'
model = onnx.load(model_path)

# 获取模型的元数据字典
metadata_dict = {prop.key: prop.value for prop in model.metadata_props}

print(json.dumps(metadata_dict))

# # 修改或添加新的元数据信息
# metadata_dict['new_key'] = 'new_value'
# metadata_dict['existing_key'] = 'updated_value'

# 修改模型的元数据
meta = model.metadata_props.add()
meta.key = "model_version"
meta.value = "20240717v1"

# 示例：修改已有的元数据
for prop in model.metadata_props:
    if prop.key == "author":
        prop.value = "TonyJiangWJ"
    if prop.key == 'description':
        prop.value = '蚂蚁森林ONNX模型'


# 保存修改后的模型
output_model_path = 'updated_model.onnx'
onnx.save(model, output_model_path)

print(f"元数据信息已更新并保存到 {output_model_path}")