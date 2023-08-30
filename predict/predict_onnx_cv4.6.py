import cv2
import numpy as np

print("opencv version %s" % cv2.getVersionString())
# 加载ONNX模型
onnx_model_path = 'runs/detect/train2/weights/best.onnx'
net = cv2.dnn.readNetFromONNX(onnx_model_path)
conf_threshold = 0.7
iou_threshold = 0.5

input_width = 640
input_height = 640
# 读取和预处理图片
image_path = 'datasets/xiaoji/images/1692428022893_1.jpg'
image = cv2.imread(image_path)
img_width = image.shape[1]
img_height = image.shape[0]
desired_height = 640
scale_factor = desired_height / image.shape[0]
resized_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
# 计算填充大小
padding = (desired_height - resized_image.shape[1]) / 2

# 目标高度
desired_size = (640, 640)
# # 创建一个640x640的方形图像
# canvas = np.zeros((desired_size[1], desired_size[0], 3), dtype=np.uint8)

# # 计算粘贴的位置
# x_offset = 0
# y_offset = (desired_size[1] - resized_image.shape[0]) // 2
#
# # 将缩放后的图像粘贴到方形图像中
# canvas[y_offset:y_offset + resized_image.shape[0], x_offset:x_offset + resized_image.shape[1]] = resized_image
input_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# Resize input image
input_img = cv2.resize(input_img, (input_width, input_height))
# 保存或显示图像
# cv2.imshow("hh", input_img)
input_blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (640, 640), swapRB=True,crop=False)
net.setInput(input_blob)
# 进行推理
output_blob_names = net.getUnconnectedOutLayersNames()
print('output blob names: %s' % str(output_blob_names))
has_postprocess = 'score' in output_blob_names
print('has postprocess? %s' % str(has_postprocess))

outputs = net.forward(output_blob_names)
print(str(outputs))


def rescale_boxes(boxes):
    # Rescale boxes to original image dimensions
    input_shape = np.array([input_width, input_height, input_width, input_height])
    boxes = np.divide(boxes, input_shape, dtype=np.float32)
    boxes *= np.array([img_width, img_height, img_width, img_height])
    return boxes


def extract_boxes(predictions):
    # Extract boxes from predictions
    boxes = predictions[:, :4]

    # Scale boxes to original image dimensions
    boxes = rescale_boxes(boxes)

    # Convert boxes to xywh format
    boxes_ = np.copy(boxes)
    boxes_[..., 0] = boxes[..., 0] - boxes[..., 2] * 0.5
    boxes_[..., 1] = boxes[..., 1] - boxes[..., 3] * 0.5
    return boxes_


def process_output(output):
    predictions = np.squeeze(output[0])

    # Filter out object confidence scores below threshold
    obj_conf = predictions[:, 4]
    predictions = predictions[obj_conf > conf_threshold]
    obj_conf = obj_conf[obj_conf > conf_threshold]

    # Multiply class confidence with bounding box confidence
    predictions[:, 5:] *= obj_conf[:, np.newaxis]

    # Get the scores
    scores = np.max(predictions[:, 5:], axis=1)

    # Filter out the objects with a low score
    valid_scores = scores > conf_threshold
    predictions = predictions[valid_scores]
    scores = scores[valid_scores]

    # Get the class with the highest confidence
    class_ids = np.argmax(predictions[:, 5:], axis=1)

    # Get bounding boxes for each object
    boxes = extract_boxes(predictions)

    # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
    # indices = nms(boxes, scores, self.iou_threshold)
    indices = cv2.dnn.NMSBoxes(boxes.tolist(), scores.tolist(), conf_threshold, iou_threshold).flatten()

    return boxes[indices], scores[indices], class_ids[indices]

boxes, scores, class_ids = process_output(outputs)
print(str(boxes))
print(str(scores))
print(str(class_ids))
# 解析推理结果
# 这里需要根据模型的输出格式进行解析，具体实现会根据模型的结构而有所不同
# for depth1 in outputs:
#     print("length of depth 1: %d" % len(depth1))
#     idx = 0
#     for detection in depth1:
#         # print(str(depth2))
#         scores = detection[5:]
#         cls_id = np.argmax(scores)
#         confidence = scores[cls_id]
#         box = detection[0:4] * np.array([image.shape[1], image.shape[0], image.shape[1], image.shape[0]])
#         (x, y, w, h) = box.astype("int")
#         # print("length of depth 2: %d" % len(depth2))
#         print("values for: %d cls_id %s confidence: %.2f x: %.2f y: %.2f w: %.2f h: %.2f" % (
#             idx, str(cls_id), confidence, x, y, w, h
#         ))
#         idx += 1
# 在图像上绘制检测结果
# 这里需要使用cv2.rectangle等函数将检测结果绘制在图像上

# 显示带有检测结果的图像
# cv2.imshow('Inference Result', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
