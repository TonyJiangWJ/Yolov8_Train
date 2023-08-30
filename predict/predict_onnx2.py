
import cv2
import numpy as np

print("opencv version %s" % cv2.getVersionString())
# 加载ONNX模型
onnx_model_path = 'runs/detect/train2/weights/best.onnx'
net = cv2.dnn.readNetFromONNX(onnx_model_path)

# 读取和预处理图片
image_path = 'datasets/xiaoji/images/1692428022893_1.jpg'
image = cv2.imread(image_path)
input_blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255.0, size=(640, 640), swapRB=True,
                                   crop=False)
net.setInput(input_blob)
# 进行推理
# output_blob_names = net.getUnconnectedOutLayersNames()
outputs = net.forward()
print(str(outputs))
# 解析推理结果
# 这里需要根据模型的输出格式进行解析，具体实现会根据模型的结构而有所不同
for depth1 in outputs:
    print("length of depth 1: %d" % len(depth1))
    idx = 0
    for detection in depth1:
        # print(str(depth2))
        scores = detection[5:]
        cls_id = np.argmax(scores)
        confidence = scores[cls_id]
        box = detection[0:4] * np.array([image.shape[1], image.shape[0], image.shape[1], image.shape[0]])
        (x, y, w, h) = box.astype("int")
        # print("length of depth 2: %d" % len(depth2))
        print("values for: %d cls_id %s confidence: %.2f x: %.2f y: %.2f w: %.2f h: %.2f" % (
            idx, str(cls_id), confidence, x, y, w, h
        ))
        idx += 1
# 在图像上绘制检测结果
# 这里需要使用cv2.rectangle等函数将检测结果绘制在图像上

# 显示带有检测结果的图像
# cv2.imshow('Inference Result', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
