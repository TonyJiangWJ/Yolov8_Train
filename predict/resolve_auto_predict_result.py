import os
import shutil

# 预测出来的结果，需要用anylabeling进行校对，校对后json文件将被格式化，此时认定为当前json为正确的
root_path = r'H:/Projects/repository/datasets/ant_forest/merge202308-10/predict/incorrect'
# 指定校对后保存的位置
data_path = r'H:/Projects/repository/datasets/ant_forest/merge202308-10/'


# 判断json文件行数，超过3行则认定为已经被校对过
def is_checked(file_path):
    with open(file_path, 'r') as fr:
        line_count = len(fr.readlines())
        fr.close()
        # print(f'line count: {line_count}')
        if line_count > 3:
            return True
    return False


if not os.path.exists(data_path):
    os.mkdir(data_path)

# 将识别结果复制到原始目录，anylabeling验证之后，json文件会格式化为多行，代表已经手动验证过
files = os.listdir(root_path)
count = 0
for file in files:
    if file.endswith('json'):
        json_path = os.path.join(root_path, file)
        if is_checked(json_path):
            count += 1
            target_path = os.path.join(data_path, file)
            print(f"复制 {json_path} => {target_path}")
            shutil.copyfile(json_path, target_path)
print(f'复制了{count}个文件')
