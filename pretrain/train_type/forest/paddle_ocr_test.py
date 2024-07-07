import cv2
from paddleocr import PaddleOCR

# 指定本地模型的路径
det_model_dir = r'../../../paddle_infer/ch_PP-OCRv4_det_infer'
rec_model_dir = r'../../../paddle_infer/ch_PP-OCRv4_rec_infer'
cls_model_dir = r'../../../paddle_infer/ch_ppocr_mobile_v2.0_cls_infer'

# 初始化PaddleOCR，指定本地模型路径
ocr = PaddleOCR(det_model_dir=det_model_dir, rec_model_dir=rec_model_dir, cls_model_dir=cls_model_dir,
                use_angle_cls=True, lang='ch')

# 读取图片
image_path = r'E:\Repository\Yolov8_Train\data\forest_20240625\16929407681109.jpg'
image = cv2.imread(image_path)

# 定义截图区域（例如，左上角坐标为(x1, y1)，右下角坐标为(x2, y2)）
x1, y1, x2, y2 = int(91.6638708114624), int(379.4771015167236), int(177.52325592041015), int(470.6386636734009)

# 截图区域
cropped_image = image[y1:y2, x1:x2]

# 保存截图区域（可选）
# cv2.imwrite('cropped_image.jpg', cropped_image)

# 使用PaddleOCR识别截图区域中的文本
result = ocr.ocr(cropped_image, cls=True)

# 提取文字
extracted_text = []
for line in result:
    for word in line:
        if len(word) > 1:
            extracted_text.append(word[1])

# 打印提取的文字
for text in extracted_text:
    print(text)

print("".join([r[0] for r in extracted_text]))

# 显示截图区域（可选）
cv2.imshow('Cropped Image', cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()