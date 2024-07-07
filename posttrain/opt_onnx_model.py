from onnxruntime.quantization import (QuantType,
                                      quantize_dynamic,
                                      # quantize_static,
                                        )
import os
from ultralytics import YOLO


def export_onnx_if_not_exists(model_path, onnx_path, overwrite=False):
    if not os.path.exists(model_path):
        raise FileExistsError('模型文件不存在:' + os.path.abspath(model_path))
    if os.path.exists(onnx_path) and overwrite is False:
        print("onnx 文件已存在")
        return
    # Load a model
    model = YOLO(model_path)
    model.export(format='onnx', opset=17, simplify=True)


def export_onnx_and_opt(model_path, overwrite=False):
    onnx_path = model_path.replace('.pt', '.onnx')
    model_quant_dynamic = onnx_path.replace('.onnx', '_lite.onnx')
    # model_quant_static = onnx_path.replace('.onnx', '_lite_s.onnx')
    export_onnx_if_not_exists(model_path, onnx_path, overwrite)
    # 动态量化
    # preprocess_onnx_path = onnx_path.replace('.onnx', '_infer.onnx')
    # quant_pre_process(onnx_path, preprocess_onnx_path)
    quantize_dynamic(
        model_input=onnx_path,  # 输入模型
        model_output=model_quant_dynamic,  # 输出模型
        weight_type=QuantType.QUInt8,  # 参数类型 Int8 / UInt8
        # 是否优化模型
    )


if __name__ == '__main__':
    # 模型路径
    # model_path = 'train/runs/detect/train15/weights/best.pt'
    # model_path = 'runs/detect/train7/weights/best.pt'
    current_model_path = '../train/runs/detect/train2/weights/best.pt'
    export_onnx_and_opt(current_model_path, overwrite=True)


