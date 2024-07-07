from onnxruntime.quantization import (QuantType,
                                      quantize_dynamic,
                                      quantize_static,)

from ultralytics import YOLO
import os


## 需要修改ultralytics代码
###
#  #ultralytics/nn/modules/block.py
#  class C2f(nn.Module):
#     # ...
#     def forward(self, x):
#         """Forward pass through C2f layer."""
#         # CHANGED
#         # y = list(self.cv1(x).chunk(2, 1))
#         # y.extend(m(y[-1]) for m in self.m)
#         # return self.cv2(torch.cat(y, 1))
#         # CHANGED
#         print("ook")
#         x = self.cv1(x)
#         x = [x, x[:, self.c:, ...]]
#         x.extend(m(x[-1]) for m in self.m)
#         x.pop(1)
#         return self.cv2(torch.cat(x, 1))
#
#  #ultralytics/nn/modules/head.py
#  class Detect(nn.Module):
#     def forward(self, x):
#         """Concatenates and returns predicted bounding boxes and class probabilities."""
#         for i in range(self.nl):
#             x[i] = torch.cat((self.cv2[i](x[i]), self.cv3[i](x[i])), 1)
#         if self.training:  # Training path
#             return x
#
#         # Inference path
#         shape = x[0].shape  # BCHW
#
#         # 转成ncnn格式时，请使用以下两行
# ##      #CHANGED
#         pred = torch.cat([xi.view(shape[0], self.no, -1) for xi in x], 2).permute(0, 2, 1)
#         return pred
# ##      #CHANGED
##

if __name__ == '__main__':
    # 模型路径
    # model_path = 'train/runs/detect/train15/weights/best.pt'
    # model_path = 'runs/detect/train7/weights/best.pt'
    # model_path = 'train/runs/detect/train12/weights/best.pt'
    model_path = os.path.abspath(r'../train/runs/detect/train27/weights/best.pt')
    # model_path = 'train/runs/detect/train6/weights/best.pt'
    # model_path = 'train/yolov8n.pt'
    # model_path = '/Users/jiangwenjie/Documents/Repositories/Github/Ant-Forest/config_data/forest_lite.onnx'

    model = YOLO(model_path)
    # model.export(format='ncnn', opset=13, simplify=True, imgsz=480)
    success = model.export(task="detect", format="onnx", opset=12, imgsz=320, simplify=True)

    # 量化模型无法正常转换成ncnn模型
    # onnx_path = model_path.replace('.pt', '.onnx')
    # model_quant_dynamic = onnx_path.replace('.onnx', '_lite.onnx')
    # quantize_dynamic(
    #     model_input=onnx_path,  # 输入模型
    #     model_output=model_quant_dynamic,  # 输出模型
    #     weight_type=QuantType.QUInt8,  # 参数类型 Int8 / UInt8
    # )
    # 输出后前往网站进行转换
    # https://convertmodel.com/
