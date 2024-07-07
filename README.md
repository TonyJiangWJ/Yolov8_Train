# YOLOv8 训练用骨架工程

- 使用 YOLOv8 训练自己的数据集
- 改造自：[https://github.com/prophet-mu/YOLOv8_Train_Guide](https://github.com/prophet-mu/YOLOv8_Train_Guide)
- 原作者相关使用说明：[语雀(prophet-mu)](https://www.yuque.com/prophetmu/chenmumu/m3axpi)
- 非常感谢 @prophet-mu 的这个仓库带我入门yolo

## 环境准备

- 建议使用Anaconda创建虚拟环境，具体安装可以网上搜索或者[上B站学习](https://www.bilibili.com/video/BV1V4411A7wG/)
- 环境搭建完毕之后安装pytorch和cuda环境，具体参考上面语雀文档中的说明，如果无GPU可以不安装cuda直接用CPU训练也可以只是慢很多。
- conda创建虚拟环境，用于Yolo训练，记得切换

## 准备训练数据

### 创建数据集

- 将数据集保存到data/{识别类型}
  - 例如识别蚂蚁森林，识别类型定义为 forest 则保存到 datasets/forest 下面 
- 对于数据集标注，建议使用anylabeling工具进行标注，标注完成后将得到图片和对应的json标注信息
- 数据集保存完毕后修改 `convert_to_yolo_txt.py` 然后运行他，将json转换成yolo标注的txt文件
  ```python
  # 初始化训练集时，指定为空数组，将自动统计并打印所有标签
  specific_labels = []
  # 指定原始目录和保存目录 保存目录为datasets下面
  root_path = './data/forest'
  target_path = './datasets/forest'
  ```
- 运行完毕后将打印出当前数据集中的所有标签信息，复制保存后面会用到

### 分割数据集为：train\val\test三个部分

- 修改 `split.py` 然后运行它，将 `datasets/forest` 中的数据集进行拆分
  ```python
  root_path = "./datasets"
  source_train_type = 'forest'
  target_train_type = 'forest'
  ```

### 创建配置文件

- 在config目录下创建自己的训练配置文件，例如forest.yaml
  ```yaml
  # Train/val/test sets as 1) dir: path/to/imgs, 2) file: path/to/imgs.txt, or 3) list: [path/to/imgs1, path/to/imgs2, ..]
  # 数据集所在位置，建议使用绝对路径
  path: E:/Repository/YOLOV8_train/datasets/forest
  train: # train images (relative to 'path')  16551 images
    - ./train
  val: # val images (relative to 'path')  4952 images
    ./val
  test: # test images (optional)
    ./test
  # Classes
  # 设置标签值，注意如果需要持续训练优化模型，这些标签的顺序不能修改，否则需要重头开始训练。新增标签可以一直往后增加
  names:
    0: cannot
    1: collect
    2: countdown
    3: help_revive
    4: item
    5: tree
    6: water
    7: waterBall
    8: stroll_btn
    9: sea_ball
    10: sea_garbage
  ```

## 开始训练

- 有两种方式可以进行训练，一种是通过命令行，另一种是python代码 选择自己喜欢的方式即可

### 命令行方式

- 打开终端，输入如下命令，具体参数说明见官网
  ```shell
  yolo task=detect mode=train model=yolov8n.pt data=config/forest.yaml batch=-1 epochs=20
  ```
- 训练完毕后会将模型保存到 `runs/detect/train/weights/best.pt` 中
- 如果增加了数据集，需要在原有模型基础上继续训练，则修改命令如下
  ```shell
  # 指定model为上一次训练的结果
  yolo task=detect mode=train model=runs/detect/train/weights/best.pt data=config/forest.yaml batch=-1 epochs=100
  ```
  
### python方式

- 创建 `train.py` 添加如下内容：
  ```python
  from ultralytics import YOLO
  
  if __name__ == '__main__':
      # Load a model
      model = YOLO(r'yolov8n.pt')  # load a pretrained model (recommended for training)
  
      # Train the model
      results = model.train(data='./config/forest.yaml', epochs=20, imgsz=640, device=0, batch=-1)
  ```
- 训练完毕后会将模型保存到 `runs/detect/train/weights/best.pt` 中
- 如果增加了数据集，需要在原有模型基础上继续训练，则修改代码如下
  ```python
  from ultralytics import YOLO
  
  if __name__ == '__main__':
      # 指定上一次训练的结果
      model = YOLO('runs/detect/train/weights/best.pt')
  
      # Train the model
      results = model.train(data='./config/forest.yaml', epochs=20, imgsz=640, device=0, batch=-1)
  ```
  
## 使用训练后模型预测

### 如果直接在本机预测，可以直接使用pt模型

- 需要注意，预测图片的路径不能包含中文，否则opencv无法正确读取

```python
from ultralytics import YOLO  
best_model = YOLO(model='E:/Repository/YOLOV8_train/runs/detect/train/weights/best.pt')
# 指定project為當前執行目錄，否則會按settings文件中的地址進行保存
result = best_model.predict(project=project_path, source=img_path, save=False)
# 后续针对result进行处理即可，具体参考auto_predict.py即可
```

## 模型导出并量化

- 跨平台使用时，可以使用onnxruntime推理onnx模型，支持c++和java等
- 量化模型可以减小模型体积，加快模型推理速度，但是会损失一定的精度
- 修改并运行 `opt_onnx_model.py` 即可将pt模型转换成onnx模型并量化
  ```python
  if __name__ == '__main__':
    # 指定训练后的模型路径
    model_path = 'runs/detect/manor_v4/weights/best.pt'
    onnx_path = model_path.replace('.pt', '.onnx')
    model_quant_dynamic = onnx_path.replace('.onnx', '_lite.onnx')
    # 导出onnx模型
    export_onnx_if_not_exists()
    # 动态量化
    quantize_dynamic(
        model_input=onnx_path,  # 输入模型
        model_output=model_quant_dynamic,  # 输出模型
        weight_type=QuantType.QUInt8,  # 参数类型 Int8 / UInt8
        optimize_model=True  # 是否优化模型
    )
  ```

### 也可以直接使用yolo命令导出

- 将模型导出为onnx
- ```yolo task=detect mode=export model=.\runs\detect\train\weights\best.pt format=onnx opset=12```
- 然后使用python `quantize_dynamic` 进行量化处理，推荐直接使用opt_onnx_model.py一步处理