import cv2
import numpy as np
from paddleocr import PaddleOCR
import os

# 指定本地模型的路径
det_model_dir = os.path.join(os.path.dirname(__file__), r'../paddle_infer/ch_PP-OCRv4_det_infer')
rec_model_dir = os.path.join(os.path.dirname(__file__), r'../paddle_infer/ch_PP-OCRv4_rec_infer')
cls_model_dir = os.path.join(os.path.dirname(__file__), r'../paddle_infer/ch_ppocr_mobile_v2.0_cls_infer')
print(det_model_dir)
# 初始化PaddleOCR，指定本地模型路径
ocr = PaddleOCR(det_model_dir=det_model_dir, rec_model_dir=rec_model_dir, cls_model_dir=cls_model_dir,
                use_angle_cls=True, lang='ch', show_log=False)


def recognize_text(img_path, region):
    # 定义截图区域（例如，左上角坐标为(x1, y1)，右下角坐标为(x2, y2)）
    x1, y1, x2, y2 = map(int, region)
    image = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
    # cv2.imread无法处理webdav路径和中文路径
    # image = cv2.imread(img_path)
    if image is None:
        print(f"图片读取失败：{img_path}")
        return ""
    # 截图区域
    cropped_image = image[y1:y2, x1:x2]
    # 使用PaddleOCR识别截图区域中的文本
    result = ocr.ocr(cropped_image, cls=True)

    # 提取文字
    extracted_text = []
    for line in result:
        if line is None:
            continue
        for word in line:
            if len(word) > 1:
                extracted_text.append(word[1])

    # 打印提取的文字
    # for text in extracted_text:
    #     print(text)

    reco_text = "".join([r[0] for r in extracted_text])
    return reco_text