import numpy as np
import onnxruntime
import time
from onnxruntime.quantization import QuantFormat, QuantType, quantize_static

import resnet50_data_reader


def benchmark(model_path):
    session = onnxruntime.InferenceSession(model_path)
    input_name = session.get_inputs()[0].name

    total = 0.0
    runs = 10
    input_data = np.zeros((1, 3, input_size, input_size), np.float32)
    # Warming up
    _ = session.run([], {input_name: input_data})
    for i in range(runs):
        start = time.perf_counter()
        _ = session.run([], {input_name: input_data})
        end = (time.perf_counter() - start) * 1000
        total += end
        print(f"{end:.2f}ms")
    total /= runs
    print(f"Avg: {total:.2f}ms")

# 预处理 python -m onnxruntime.quantization.preprocess --input mobilenetv2-7.onnx --output mobilenetv2-7-infer.onnx
# 预处理 python -m onnxruntime.quantization.preprocess --input best.onnx --output best-infer.onnx
def main():
    input_model_path = '../runs/detect/forest_v4_320_try/weights/best-infer.onnx'
    output_model_path = input_model_path.replace('.onnx', '_lite.onnx')
    calibration_dataset_path = '../datasets/forest2/static'
    dr = resnet50_data_reader.ResNet50DataReader(
        calibration_dataset_path, input_model_path
    )

    # Calibrate and quantize model
    # Turn off model optimization during quantization
    quantize_static(
        input_model_path,
        output_model_path,
        dr,
        activation_type=QuantType.QUInt8,
        quant_format=QuantFormat.QDQ,
        per_channel=True,
        weight_type=QuantType.QUInt8,
        optimize_model=True,
    )
    print("Calibrated and quantized model saved.")

    print("benchmarking fp32 model...")
    benchmark(input_model_path)

    print("benchmarking int8 model...")
    benchmark(output_model_path)


if __name__ == "__main__":
    input_size = 320
    main()
