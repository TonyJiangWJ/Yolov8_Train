import os
import shutil
root_path = 'H:/Projects/repository/datasets/feed/predict'
data_path = 'H:/Projects/repository/datasets/feed'


def is_checked(file_path):
    with open(file_path, 'r') as fr:
        line_count = len(fr.readlines())
        fr.close()
        print(f'line count: {line_count}')
        if line_count > 3:
            return True
    return False

if not os.path.exists(data_path):
    os.mkdir(data_path)

# 将识别结果复制到原始目录，anylabeling验证之后，json文件会格式化为多行，代表已经手动验证过
files = os.listdir(root_path)
for file in files:
    if file.endswith('json'):
        json_path = os.path.join(root_path, file)
        if is_checked(json_path):
            target_path = os.path.join(data_path, file)
            print(f"复制 {json_path} => {target_path}")
            shutil.copyfile(json_path, target_path)
