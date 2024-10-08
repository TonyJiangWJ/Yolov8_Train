import cv2
import numpy as np
import json

# 读取彩色图像
image = cv2.imread(r'E:\Repository\Yolov8_Train\data\forest\16930051701859.jpg')
json_path = r"E:\Repository\Yolov8_Train\data\forest\16930051701859.json"
colorstr1 = '#9BDA00'
colorstr2 = '#E1FF2F'


def image_check():
    # 将颜色值从字符串转换为BGR格式
    color1 = np.array(tuple(int(colorstr1[i:i + 2], 16) for i in (1, 3, 5)))[::-1]
    color2 = np.array(tuple(int(colorstr2[i:i + 2], 16) for i in (1, 3, 5)))[::-1]

    # 确保color1是较小的值，color2是较大的值
    lower_bound = np.minimum(color1, color2)
    upper_bound = np.maximum(color1, color2)

    # 使用inRange函数进行二值化处理
    binary_image = cv2.inRange(image, lower_bound, upper_bound)

    with open(json_path, 'r') as f:
        content = json.load(f)
        f.close()
    shapes = content['shapes']
    for shape in shapes:
        points = shape['points']
        # 定义感兴趣区域（ROI）的坐标
        # x, y, w, h = 100, 100, 200, 200  # 例如，ROI的左上角坐标为(100, 100)，宽度为200，高度为200
        x1, y1, x2, y2 = points[0][0], points[0][1], points[1][0], points[1][1]
        # 提取ROI
        roi = binary_image[y1:y2, x1:x2]
        roi_3 = image[y1:y2, x1:x2]
        # 计算二值化图像的直方图
        hist = cv2.calcHist([roi], [0], None, [256], [0, 256])

        # 计算直方图的平均值
        hist_sum = np.sum(hist)
        hist_average = np.sum(np.arange(256) * hist.flatten()) / hist_sum

        print(f'label:{shape["label"]} Hist Average: {hist_average}')
        # 将单通道图像重新写入到三通道图像的原始位置中
        # 创建一个与ROI大小相同的全零三通道图像
        roi_3channel = np.zeros_like(roi_3)

        # # 将单通道图像复制到三通道图像的第一个通道（蓝色通道）
        # roi_3channel[:, :, 0] = roi

        # 将单通道图像复制到三通道图像的所有通道
        roi_3channel[roi == 255] = [255, 255, 255]

        # 将处理后的ROI放回原图像中
        image[y1:y2, x1:x2] = roi_3channel

    # 显示二值化后的图像
    cv2.imshow('Binary Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 保存二值化后的图像
    # cv2.imwrite('binary_image.jpg', binary_image)


def hough_circles():

    # 将图像转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用高斯模糊来减少噪声
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # 使用霍夫变换检测圆形
    circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=30, maxRadius=90)

    # 如果检测到圆形，绘制它们
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            print(f"x,y={i[0]},{i[1]} radius:{i[2]:.2f}")
            # 绘制圆形
            cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # 绘制圆心
            cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)

    # 显示结果图像
    cv2.imshow('Detected Circles', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# image_check()
hough_circles()