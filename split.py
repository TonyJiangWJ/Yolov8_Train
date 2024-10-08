# 将图片和标注数据按比例切分为 训练集和测试集
import shutil
import random
import os

image_original_path = ''
label_original_path = ''
train_image_path = ''
train_label_path = ''
val_image_path = ''
val_label_path = ''
test_image_path = ''
test_label_path = ''


def make_empty_dir(target_dir):
    if os.path.exists(target_dir):
        print("rm tree:", target_dir)
        try:
            shutil.rmtree(target_dir)
        except:
            print(f"failed to remove dir {target_dir}")
    os.makedirs(target_dir)


# 检查文件夹是否存在
def mkdir_and_clear():
    make_empty_dir(train_image_path)
    make_empty_dir(train_label_path)
    make_empty_dir(val_image_path)
    make_empty_dir(val_label_path)
    make_empty_dir(test_image_path)
    make_empty_dir(test_label_path)


def do_split_dataset(train_percent, val_percent, test_percent, image_type):
    mkdir_and_clear()

    total_txt = os.listdir(label_original_path)
    num_txt = len(total_txt)
    list_all_txt = range(num_txt)  # 范围 range(0, num)

    num_train = int(num_txt * train_percent)
    num_val = int(num_txt * val_percent)
    num_test = int(num_txt * test_percent)
    # 上述计算容易精度丢失，多出来的放到验证集
    num_val += num_txt - num_train - num_test - num_val

    train = random.sample(list_all_txt, num_train)
    # 在全部数据集中取出train
    val_test = [i for i in list_all_txt if not i in train]
    # 再从val_test取出num_val个元素，val_test剩下的元素就是test
    val = random.sample(val_test, num_val)

    print("总数：{} 训练集数目：{}, 验证集数目：{},测试集数目：{}".format(num_txt, len(train), len(val), num_test))
    print("coping...")
    for i in list_all_txt:
        name = total_txt[i][:-4]

        src_image = image_original_path + name + image_type
        src_label = label_original_path + name + '.txt'

        if i in train:
            dst_train_image = train_image_path + name + image_type
            dst_train_label = train_label_path + name + '.txt'
            shutil.copyfile(src_image, dst_train_image)
            shutil.copyfile(src_label, dst_train_label)
        elif i in val:
            dst_val_image = val_image_path + name + image_type
            dst_val_label = val_label_path + name + '.txt'
            shutil.copyfile(src_image, dst_val_image)
            shutil.copyfile(src_label, dst_val_label)
        else:
            dst_test_image = test_image_path + name + image_type
            dst_test_label = test_label_path + name + '.txt'
            shutil.copyfile(src_image, dst_test_image)
            shutil.copyfile(src_label, dst_test_label)
    print("done")


def split_dataset(train_percent, val_percent, test_percent, root_path, source_train_type, target_train_type=None,
                  image_type='.jpg'):
    global image_original_path, label_original_path, train_image_path, train_label_path, val_image_path, val_label_path, test_image_path, test_label_path
    if target_train_type is None:
        target_train_type = source_train_type
    # 数据集路径
    image_original_path = root_path + '/%s/images/' % source_train_type
    label_original_path = root_path + '/%s/labels/' % source_train_type
    # 训练集路径
    train_image_path = root_path + '/%s/train/images/' % target_train_type
    train_label_path = root_path + '/%s/train/labels/' % target_train_type
    # 验证集路径
    val_image_path = root_path + '/%s/val/images/' % target_train_type
    val_label_path = root_path + '/%s/val/labels/' % target_train_type
    # 测试集路径
    test_image_path = root_path + '/%s/test/images/' % target_train_type
    test_label_path = root_path + '/%s/test/labels/' % target_train_type
    do_split_dataset(train_percent, val_percent, test_percent, image_type)


if __name__ == '__main__':
    # 数据集划分比例，训练集70%，验证集15%，测试集15%，按需修改
    train_percent = 0.7
    val_percent = 0.15
    test_percent = 0.15
    root_path = "./datasets"
    source_train_type = 'forest_recheck_20240714'
    split_dataset(train_percent, val_percent, test_percent, root_path, source_train_type)
