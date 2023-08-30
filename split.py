# 将图片和标注数据按比例切分为 训练集和测试集
import shutil
import random
import os

# 数据集划分比例，训练集70%，验证集15%，测试集15%，按需修改
train_percent = 0.70
val_percent = 0.15
test_percent = 0.15


def make_empty_dir(target_dir):
    if os.path.exists(target_dir):
        print("rm tree:", target_dir)
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)


# 检查文件夹是否存在
def mkdir_and_clear():
    make_empty_dir(train_image_path)
    make_empty_dir(train_label_path)
    make_empty_dir(val_image_path)
    make_empty_dir(val_label_path)
    make_empty_dir(test_image_path)
    make_empty_dir(test_label_path)


def main():
    mkdir_and_clear()

    total_txt = os.listdir(label_original_path)
    num_txt = len(total_txt)
    list_all_txt = range(num_txt)  # 范围 range(0, num)

    num_train = int(num_txt * train_percent)
    num_val = int(num_txt * val_percent)
    num_test = num_txt - num_train - num_val

    train = random.sample(list_all_txt, num_train)
    # 在全部数据集中取出train
    val_test = [i for i in list_all_txt if not i in train]
    # 再从val_test取出num_val个元素，val_test剩下的元素就是test
    val = random.sample(val_test, num_val)

    print("训练集数目：{}, 验证集数目：{},测试集数目：{}".format(len(train), len(val), num_test))
    for i in list_all_txt:
        name = total_txt[i][:-4]

        srcImage = image_original_path + name + image_type
        srcLabel = label_original_path + name + '.txt'

        if i in train:
            dst_train_Image = train_image_path + name + image_type
            dst_train_Label = train_label_path + name + '.txt'
            shutil.copyfile(srcImage, dst_train_Image)
            shutil.copyfile(srcLabel, dst_train_Label)
        elif i in val:
            dst_val_Image = val_image_path + name + image_type
            dst_val_Label = val_label_path + name + '.txt'
            shutil.copyfile(srcImage, dst_val_Image)
            shutil.copyfile(srcLabel, dst_val_Label)
        else:
            dst_test_Image = test_image_path + name + image_type
            dst_test_Label = test_label_path + name + '.txt'
            shutil.copyfile(srcImage, dst_test_Image)
            shutil.copyfile(srcLabel, dst_test_Label)


if __name__ == '__main__':
    root_path = "./datasets"
    train_type = 'feed'
    target_train_type = 'feed'
    image_type = '.jpg'
    # 数据集路径
    image_original_path = root_path + '/%s/images/' % train_type
    label_original_path = root_path + '/%s/labels/' % train_type
    # 训练集路径
    train_image_path = root_path + '/%s/train/images/' % target_train_type
    train_label_path = root_path + '/%s/train/labels/' % target_train_type
    # 验证集路径
    val_image_path = root_path + '/%s/val/images/' % target_train_type
    val_label_path = root_path + '/%s/val/labels/' % target_train_type
    # 测试集路径
    test_image_path = root_path + '/%s/test/images/' % target_train_type
    test_label_path = root_path + '/%s/test/labels/' % target_train_type
    main()
