import cv2
import numpy as np


def interval_img(img, region, color_lower, color_upper):
    """
    img Mat
    region [x1,y1,x2,y2]
    color_lower #000000
    color_upper #ffffff
    """
    # 将颜色值从字符串转换为BGR格式
    color1 = np.array(tuple(int(color_lower[i:i + 2], 16) for i in (1, 3, 5)))[::-1]
    color2 = np.array(tuple(int(color_upper[i:i + 2], 16) for i in (1, 3, 5)))[::-1]

    # 确保color1是较小的值，color2是较大的值
    lower_bound = np.minimum(color1, color2)
    upper_bound = np.maximum(color1, color2)

    x1, y1, x2, y2 = map(int, region)
    # 提取范围y1:y2, x1:x2
    iou = img[y1:y2, x1:x2]
    # 使用inRange函数进行二值化处理
    return cv2.inRange(iou, lower_bound, upper_bound)


def get_hist_avg(img, region, color_lower='#9BDA00', color_upper='#E1FF2F'):
    tmp_img = interval_img(img, region, color_lower, color_upper)
    # 计算二值化图像的直方图
    hist = cv2.calcHist([tmp_img], [0], None, [256], [0, 256])

    # 计算直方图的平均值
    hist_sum = np.sum(hist)
    return np.sum(np.arange(256) * hist.flatten()) / hist_sum
