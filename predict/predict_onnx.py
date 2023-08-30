import cv2
import numpy as np
import onnxruntime as ort

# yolo task=detect mode=predict model=runs/detect/train2/weights/best.onnx source=datasets/xiaoji/images/1692428022893_1.jpg
# 加载ONNX模型
onnx_model_path = 'runs/detect/train2/weights/best.onnx'
ort_session = ort.InferenceSession(onnx_model_path)

# 读取和预处理图片
image_path = 'datasets/xiaoji/images/1692428022893_1.jpg'
image = cv2.imread(image_path)
resized_image = cv2.resize(image, (640, 640))
input_data = np.transpose(resized_image, (2, 0, 1))
input_data = np.expand_dims(input_data, axis=0)
input_data = input_data.astype(np.float32) / 255.0
model_h, model_w = ort_session.get_inputs()[0].shape[2:]
# 进行推理
print("模型輸入參數：%s input width: %d height: %d" % (ort_session.get_inputs()[0].name, model_w, model_h))
ort_inputs = {ort_session.get_inputs()[0].name: input_data}
ort_outputs = ort_session.run(None, ort_inputs)
for depth1 in ort_outputs:
    print("length of depth 1: %d" % len(depth1))
    for depth2 in depth1:
        print("length of depth 2: %d" % len(depth2))
        idx = 0
        for depth3 in depth2:
            print("values for: %d" % idx)
            idx += 1
            for v in depth3:
                if v > 0.5:
                    print(str(v))
            # print(str(depth3))
            # print("length of depth 3: %d" % len(depth3))
# print('推理结果' + str(ort_outputs))
# result = ort_outputs[0]
# print('length of result: %d' % len(result))
# # 解析输出
# output_boxes = result[0]
# print("boxes: %s" % str(output_boxes))
# print('length of boxes: %d' % len(result))
# output_confidences = result[1]
# print("output_confidences: %s" % str(output_confidences))
# output_class_probs = result[2]
# print("output_class_probs: %s" % str(output_class_probs))

# 后处理输出，绘制边界框
# 这部分需要根据YOLO模型的输出结构进行解析，具体实现取决于YOLO版本
# 通常涉及置信度阈值、NMS（非极大值抑制）等操作

# 在图片上绘制边界框和类别信息
# 这部分也需要根据模型输出的格式进行绘制
# 可以使用cv2.rectangle和cv2.putText等函数

# 显示处理后的图片
# cv2.imshow('Inference Result', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
