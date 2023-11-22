from predict.copy_labeled_data import copy_labeled_data

# 将新标签数据集合旧标签数据集合并
# 相当于旧标签数据集是一个大的，在新标签模型训练完毕之后，需要使用完整的数据集进行回归训练 否则容易丢失精度
if __name__ == '__main__':
    copy_count = 0
    # 新标签数据集
    new_root_path = r'K:/YOLOV8_train_clean/data/manor_1124'
    # 旧标签数据集
    old_data_path = 'K:/YOLOV8_train_clean/data/manor'

    copy_count = copy_labeled_data(new_root_path, new_root_path, old_data_path,
                                   overwrite=False,
                                   _copy_count=copy_count)
    print(f'复制了{copy_count}个标注数据')
