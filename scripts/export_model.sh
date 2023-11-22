# 指定任务为目标检测，模式为导出模型，指定训练后到pt模型地址，指定导出格式为onnx
yolo task=detect mode=export model=.\runs\detect\train\weights\best.pt format=onnx opset=11

yolo task=detect mode=export model=.\runs\detect\train2\weights\best.pt format=onnx opset=12
#opencv-python==4.6.0

yolo task=detect mode=export model=.\runs\detect\train3\weights\best.pt format=onnx opset=12

yolo task=detect mode=export model=.\runs\detect\train4\weights\best.pt format=onnx opset=12

yolo task=detect mode=export model=.\runs\detect\train5\weights\best.pt format=onnx opset=12

yolo task=detect mode=export model=.\runs\detect\train6\weights\best.pt format=onnx opset=12

yolo task=detect mode=export model=.\runs\detect\train7\weights\best.pt format=onnx opset=12


yolo task=detect mode=export model=.\runs\detect\manor_v4\weights\best.pt format=onnx opset=12

yolo task=detect mode=export model=.\runs\detect\feed_v3\weights\best.pt format=onnx opset=12
# 训练时的使用大图，导出可以指定小图
yolo task=detect mode=export model=.\runs\detect\feed_v3\weights\best.pt format=onnx opset=12 imgsz=320

# 蚂蚁森林
yolo task=detect mode=export model=.\runs\detect\forest_v3\weights\best.pt format=onnx opset=12 imgsz=320

yolo task=detect mode=export model=.\runs\detect\forest_v3_320\weights\best.pt format=onnx opset=12
yolo task=detect mode=export model=.\runs\detect\forest_v4_320\weights\best.pt format=onnx opset=12