import json
import xml.etree.ElementTree as ET

# 读取 AnyLabeling 的 JSON 数据
with open('yuanshen/frame_sec_1.0.json', 'r') as json_file:
    data = json.load(json_file)

# 定义 VOC XML 文件的根节点
root = ET.Element('annotation')

# 添加文件名元素
filename = ET.SubElement(root, 'filename')
filename.text = data['imagePath']   # 替换为实际的图像文件名

# 添加图像尺寸元素
size = ET.SubElement(root, 'size')
width = ET.SubElement(size, 'width')
width.text = str(data['imageWidth'])  # 替换为实际图像宽度
height = ET.SubElement(size, 'height')
height.text = str(data['imageHeight'])  # 替换为实际图像高度

# 遍历 JSON 数据中的标注对象
for annotation in data['shapes']:
    # 获取标注的类别和边界框信息
    label = annotation['label']
    points = annotation['points']
    x_min = min(p[0] for p in points)
    y_min = min(p[1] for p in points)
    x_max = max(p[0] for p in points)
    y_max = max(p[1] for p in points)

    # 创建对象元素
    obj = ET.SubElement(root, 'object')
    name = ET.SubElement(obj, 'name')
    name.text = label
    difficult = ET.SubElement(obj, 'difficult')
    difficult.text = '0'

    # 创建边界框元素
    bndbox = ET.SubElement(obj, 'bndbox')
    xmin = ET.SubElement(bndbox, 'xmin')
    xmin.text = str(int(x_min))
    ymin = ET.SubElement(bndbox, 'ymin')
    ymin.text = str(int(y_min))
    xmax = ET.SubElement(bndbox, 'xmax')
    xmax.text = str(int(x_max))
    ymax = ET.SubElement(bndbox, 'ymax')
    ymax.text = str(int(y_max))

# 将 XML 树保存到文件
tree = ET.ElementTree(root)
tree.write('output.xml')
# 将 ElementTree 转换为字符串
xml_string = ET.tostring(root, encoding='utf8', method='xml')

# 打印字符串
print(xml_string.decode('utf8'))  # 将字节串解码为字符串并打印

print('Conversion complete. VOC XML file saved as output.xml')